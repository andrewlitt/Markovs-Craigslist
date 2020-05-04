# Markovs-Craigslist

Generating fake Craigslist 'missed connections' posts using [Markov Chains](https://en.wikipedia.org/wiki/Markov_chain). A fun webscrape mini-project written in Python.

Packages used:
- [Markovify](https://github.com/jsvine/markovify)
- [Requests](https://2.python-requests.org/en/master/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Natural Language Toolkit](https://www.nltk.org/)

Main script is in /scraping. Rest is the CRA site to generate posts for users.

Scraping script is exposed as a CLI using the [python-fire](https://github.com/google/python-fire) library.

Running:
```
pip install -r requirements.txt
python craigslist.py generate
```

Model outputs are sent to the command line!