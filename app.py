from flask import Flask, render_template, request, redirect
import pymongo
import os 
from dotenv import load_dotenv
from pymongo import MongoClient

app = Flask(__name__)


# cluster = MongoClient()
load_dotenv()
MONGO_URI   = os.getenv("MONGO_URI")
cluster = MongoClient(MONGO_URI)


# Database name
db = cluster['weekly_report']


# Collection name
collection = db['intern_id']
score = db['report']
 

@app.route("/", methods=["GET", "POST"])
def submit():
    
    intern       = request.form.get('intern_id')
    rating        = request.form.get('rating')
    comments      = request.form.get('review_d')

    
    new_report_id = get_last_report_id()
    collection.insert_one(
        {'intern_id': intern, 'rating': rating, 'comments': comments, 'report_id':new_report_id })

    
    return render_template('review.html')

def get_last_report_id():
    
    last_report_id = collection.find().sort([('report_id',-1)]).limit(1)
    try:
        last_report_id = last_report_id[0]['report_id']
    except:
        last_report_id = 0

    return last_report_id + 1



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")