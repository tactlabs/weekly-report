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
    
    intern              = request.form.get('intern_id')
    rating              = request.form.get('rating')
    comments            = request.form.get('review_d')
    reviewer_name       = request.form.get('reviewer_name')
    date                = request.form.get('date')
 
    
    new_report_id = get_last_report_id()
    
    collection.insert_one(
        {'intern_id': intern, 'rating': rating, 'comments': comments, 'reviewer_name': reviewer_name, 'date': date, 'report_id':new_report_id })

    
    return render_template('review.html')

def get_last_report_id():
    
    last_report_id = collection.find().sort([('report_id',-1)]).limit(1)
    try:
        last_report_id = last_report_id[0]['report_id']
    except:
        last_report_id = 0

    return last_report_id + 1


def get_page(request):

    page = request.values.get("page")

    if(not page):
        page = "1"

    page = int(page) 

    return page

@app.route('/entries')
def all_entries():

    page_size = 10
    
    starting_id = collection.find().sort('_id', pymongo.ASCENDING)

    page_no = get_page(request)

    try:
        last_id = starting_id[(page_no - 1) * page_size]['_id']
    except:
        None
    
    all_links = collection.find({
        '_id':{'$gte':last_id}
    }).sort('_id', pymongo.ASCENDING).limit(page_size)

    result = []

    for data in all_links:
        del data['_id']
        result.append(data)
    
    try:
    
        last_id = starting_id[(page_no * page_size)+1]['_id']

        next_page = page_no + 1 
       

    except:
        next_page = None

    if(page_no == 1):
        prev_page = None

    else:
        prev_page = page_no - 1

    result_data = {
        "result"            : result,
        "current_page"      : page_no,
        "next_page"         : next_page,
        "prev_page"         : prev_page
    }       

    if("result" in result_data):

        result_data["result"] = result
        
    else:
        result_data = {}
        
        result_data["current_page"] = 1
    
    return render_template('entries.html', result = result_data, data = result_data["result"])
    

@app.route("/review/<report_id>", methods=['GET'])

def get_info(report_id):
    
    all_links = collection.find_one({'report_id': int(report_id)})
    
    return render_template('display.html' , result = all_links )

    


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")