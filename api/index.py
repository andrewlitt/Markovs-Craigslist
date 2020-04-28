from http.server import BaseHTTPRequestHandler, HTTPServer
import markovify
import json
import random

class handler(BaseHTTPRequestHandler):
   def do_GET(self):
      self.send_response(200)
      self.send_header("Content-type", "text/json")
      self.end_headers()
      print(self.wfile)
      with open('./data/master_model.json') as master_model:
         data = json.load(master_model)

      model = json.dumps(data.get('title'))
      master_title_model = markovify.Text.from_json(model)
      output = master_title_model.make_sentence(tries = 100)

      master_sentence_models = []
      num_models = len(data['sentences'])

      for i in range(num_models):
         model = json.dumps(data.get('sentences')[i])
         master_sentence_models.append(markovify.Text.from_json(model))

      title_output = master_title_model.make_sentence(tries = 100)
      sentence_output = []
      for i in range(random.randint(3,num_models)):
         s = master_sentence_models[i].make_sentence(tries = 100)
         if(s != None):
            sentence_output.append(s)

      output = {
         'title': title_output,
         'sentences': sentence_output
      }

      self.wfile.write(json.dumps(output).encode(encoding='utf_8'))
      self.wfile.close()
      return