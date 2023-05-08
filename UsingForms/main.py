from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# set up the MongoClient
client = MongoClient('mongodb://localhost:27017/')

# connect to the database
db = client['mydatabase']
messages_collection = db['messages']


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form",  methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        print("Inputed data: ",name, message)

    return render_template('form.html')

@app.route('/display', methods=['GET', 'POST'])
def display():
    name = request.form['name']
    message = request.form['message']
    return render_template('display.html', name=name, message=message)

if __name__ == "__main__":
    app.run()
