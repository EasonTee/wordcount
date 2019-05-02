import requests
import operator
import re
import nltk
from app.stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
from worker import conn

def count_and_save_words(url):
    errors = []
    
    try:
        r = requests.get(url)
            
    except:
        errors.append(
            "Unable to get URL. Please make sure it is valid and try again"
            )
        return {"error":errors}

        
    # text processing
    #  beautifulsoup to clean the text, by removing the HTML tags
    raw = BeautifulSoup(r.text,'html.parser').get_text()  
    nltk.data.path.append('./nltk_data/') #set the path to find punkt file
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
    try:
        from app.models import Result
        from app import db
        result = Result(
        url=url,
        result_all = raw_word_count,
        result_no_stop_words=no_stop_words_count
        )
        db.session.add(result)
        db.session.commit()
        return result.id
                
    except:
        errors.append("unable to add item to database.")