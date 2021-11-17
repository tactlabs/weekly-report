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
    
@app.route('/')
def my_form():
    
    return render_template('submit.html')


@app.route("/", methods=["GET", "POST"])
def submit():
    
    intern_id       = request.form.get('intern_id')
    # paper_link  = request.form.get('paper_link')
    
    new_report_id = get_last_report_id()
    collection.insert_one(
        {'intern_id': intern_id, 'report_id':new_report_id })

    
    return render_template('submit.html')

def get_last_report_id():
    
    last_report_id = collection.find().sort([('report_id',-1)]).limit(1)
    try:
        last_report_id = last_report_id[0]['report_id']
    except:
        last_report_id = 0

    return last_report_id + 1


@app.route('/interns')
def choose_paper():
    
    all_interns = collection.find({})
    result = []
    for data in all_interns:
        del data['_id']
        result.append(data)
        
    
    return render_template('interns.html', result = result)


@app.route("/review/<report_id>", methods=['GET'])

def get_info(report_id):
    
    all_interns = collection.find_one({'report_id': int(report_id)})
    return render_template('review.html' , result = all_interns )


@app.route("/review/submit", methods=['POST'])
def review():

    if request.method == 'POST':
        
        report_id        = request.form.get('report_id')
        
        rating        = request.form.get('rating')
        comments      = request.form.get('review_d')

        intern_id= collection.find({'report_id': int(report_id)})

        try:

             for item in intern_id:
                intern_id = item['report_id']
                current_data = { 'reference': intern_id, 'rating': rating, 'comments': comments }
                score.insert_one(current_data)
                
                print(current_data)
        
        except:
            
            return "Intern Doesn't Exist"
        

    return redirect(f'/review/{report_id}')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")