<<<<<<< HEAD
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
=======
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import requests
import operator
import re
import nltk
from app.stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
>>>>>>> tester

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app.models import Result


<<<<<<< HEAD
@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)
=======
@app.route('/', methods=['GET','POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            url = request.form['url']
            r = requests.get(url)
            
        except:
            errors.append(
                "Unable to get URL. Please make sure it is valid and try again"
                )
            return render_template('index.html',errors = errors, results = results)

        if r:
            # text processing
            #  beautifulsoup to clean the text, by removing the HTML tags
            raw = BeautifulSoup(r.text,'html.parser').get_text()  
            nltk.data.path.append('./nltk_data/') #set the path
            tokens = nltk.word_tokenize(raw) # Tokenize the raw text (break up the text into individual words)
            text = nltk.Text(tokens) # Turn the tokens into an nltk text object.

            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*') # regular expression that matched anything not in the standard alphabet
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)
            # save the result
            results = sorted(
                no_stop_words_count.items(),
                key = operator.itemgetter(1),
                reverse = True
                )[:10]
            try:
                result = Result(
                url=url,
                result_all = raw_word_count,
                result_no_stop_words=no_stop_words_count
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("unable to add item to database.")
    return render_template('index.html',errors = errors, results = results)




>>>>>>> tester
