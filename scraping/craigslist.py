import fire
import glob, os
import json
import requests
import markovify
import random
import re
from datetime import datetime
from bs4 import BeautifulSoup
from nltk import tokenize

class MarkovsCraigslist(object):

    def make_model(self, city_name):
        # Figure out how many pages there are
        r = requests.get(f'https://{city_name}.craigslist.org/search/mis')
        content = BeautifulSoup(r.content,'html.parser')
        total_count = int(content.find(class_='totalcount').string)
        num_pages = total_count//120+1;

        # Initialize Markov chain models using Markovify. Using silly dummy sentences to start.
        title_model = markovify.Text("Looking for a guy named John Doe")
        location_model = markovify.Text("Main st.")
        text_model = markovify.Text("Met John the other day, have you seen him?")
        sentence_models = []

        # For all the pages of missed connections
        for page in range(num_pages):

            # Get the post list page, parse it with Beautifulsoup
            url = f'https://{city_name}.craigslist.org/search/mis?s={120*page}'
            r = requests.get(url)
            content = BeautifulSoup(r.content,'html.parser')

            # For each post link in the list
            for postNum, post in enumerate(content.find_all('a',class_='result-title')):

                # Get the actual post
                url = post.get('href')
                r = requests.get(url)
                post_content = BeautifulSoup(r.content,'html.parser')
                post_meta = post_content.find(class_='postingtitletext')

                # If the post exists (Sometimes the link leads to a post that has been removed)
                if post_meta:
                    # Extract and add Title to model
                    post_title = post_meta.find(id ='titletextonly').string
                    post_title = re.sub('[|]|:|-|;|"|(\(|\))|(\[|\])|[\.][\.][\.]|[\']','',post_title)
                    title =  markovify.Text(post_title)
                    title_model = markovify.combine(models=[title_model, title])

                    # The following lines are bad code, but BeautifulSoup can't seem to extract the post text easily.
                    post_text = post_content.find(id='postingbody')
                    post_text = post_text.div.next_sibling.string
                    post_text = re.sub('[|]|:|-|;|"|(\(|\))|(\[|\])|[\.][\.][\.]|[\']','',post_text)
                    post_text = tokenize.sent_tokenize(post_text)
                    
                    # If the length of the post is longer than sentence models currently made
                    if len(post_text) > len(sentence_models):
                        # Add a new sentence model
                        while len(post_text) > len(sentence_models):
                            sentence_models.append(markovify.Text('I'))

                    for i, sentence in enumerate(post_text):
                        text = markovify.Text(sentence)
                        sentence_models[i] = markovify.combine(models=[sentence_models[i], text])
                    print('Processed Post ' + str(postNum+1+120*page) +'/'+ str(total_count-1)+' - ' + post_title)

        # Generate Sentences from the Model
        print('\nMARKOV GENERATED\n')
        print(title_model.make_sentence(tries = 100))
        print('\n')
        num_sentences = 4
        for i in range(num_sentences):
            s = sentence_models[i].make_sentence(tries = 100)
            if(s != 'None'):
                print(s)
        
        # Save
        date_str = datetime.today().strftime('%d_%m_%Y')
        title_output = '{ "title": ' + title_model.to_json() + ','
        with open(f'./dev-data/{city_name}_{date_str}_data.json','w') as outfile:
            outfile.write(title_output)

        sentence_outputs = '"sentences": [' + sentence_models[0].to_json()
        for i in range(len(sentence_models)-1):
            sentence_outputs = sentence_outputs+','+sentence_models[i+1].to_json()
        sentence_outputs += ']}'

        with open(f'./dev-data/{city_name}_{date_str}_data.json','a+') as outfile:
                data = sentence_models[i].to_json()
                print(type(data))
                outfile.write(sentence_outputs)
    
    def merge_models(self):
        title_model = markovify.Text("Looking for a guy named John Doe")
        sentence_models = []
        os.chdir("./dev-data")
        files =  glob.glob("*.json")
        for f in files:
            with open(f) as city_model:
                data = json.load(city_model)
                model = json.dumps(data.get('title'))
                new_title_model = markovify.Text.from_json(model)
                title_model = markovify.combine([title_model, new_title_model])

                num_models = len(data['sentences'])
                for i in range(num_models):
                    model = json.dumps(data.get('sentences')[i])
                    if(len(sentence_models) <= i):
                        sentence_models.append(markovify.Text.from_json(model))
                    else:
                        new_sentence_model = markovify.Text.from_json(model)
                        sentence_models[i] = markovify.combine([sentence_models[i], new_sentence_model])

        title_model = title_model.compile()
        s = title_model.make_sentence(tries = 100)
        print(s)

        for i in range(len(sentence_models)): 
            sentence_models[i] = sentence_models[i].compile()
            s = sentence_models[i].make_sentence(tries = 100)
            if(s != None):
                print(s)
        
        os.chdir("..")
        date_str = datetime.today().strftime('%d_%m_%Y')
        title_output = '{ "title": ' + title_model.to_json() + ','
        with open(f'./master_model.json','w') as outfile:
            outfile.write(title_output)
        sentence_outputs = '"sentences": [' + sentence_models[0].to_json()
        for i in range(len(sentence_models)-1):
            sentence_outputs = sentence_outputs+','+sentence_models[i+1].to_json()
        sentence_outputs += ']}'
        with open(f'./master_model.json','a+') as outfile:
                data = sentence_models[i].to_json()
                outfile.write(sentence_outputs)
    
    def generate(self):
        with open(f'./master_model.json') as master:
                data = json.load(master)
                model = json.dumps(data.get('title'))
                master_title_model = markovify.Text.from_json(model)
                master_sentence_models = []
                num_models = len(data['sentences'])
                for i in range(num_models):
                    model = json.dumps(data.get('sentences')[i])
                    master_sentence_models.append(markovify.Text.from_json(model))
                s = master_title_model.make_sentence(tries = 100)
                print('\n')
                print(s)
                print('\n')
                for i in range(random.randint(3,num_models)):
                    s = master_sentence_models[i].make_sentence(tries = 100)
                    if(s != None):
                        print(s)
                
if __name__ == '__main__':
    fire.Fire(MarkovsCraigslist)
