from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from rq import Queue
from rq.job import Job
from worker import conn
from app.count_and_save import *

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

q = Queue(connection = conn)

from app.models import *


@app.route('/', methods=['GET','POST'])
def index():
    results = {}

    if request.method == "POST":
        url = request.form['url']
        if 'http//' not in url[:7]:
            url = 'http//'+url
        job = q.enqueue_call(count_and_save_words,args=(url,),result_ttl=5000)
        print(job.get_id())

    return render_template('index.html', results = results)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection = conn)

    if job.is_finished:
        result = Result.query.filter_by(id = job.result).first()
        results = sorted(
            result.result_nostop_words.items(),
            key = operator.itemgetter(1),
            reverse = True
        )[:10]
        return jsonify(results)
    else:
        return "NAY!",202

    


