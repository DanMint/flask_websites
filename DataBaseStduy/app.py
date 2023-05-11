from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freinds.db'
# Initialize the DB
db = SQLAlchemy(app)

# Create DB model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Create a func to return a string when we add something
    def __repr__(self):
        return '<Name %r>' % self.id
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/friends', methods=['POST', 'GET']) 
def friends():
    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Friends(name=friend_name) 
        # push to db
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect("/friends")
        except:
            return "error adding a new friend"
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html", friends=friends)
    

@app.route('/friendList', methods=['GET'])
def friendList():
    if request.method == "GET":
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("listOfFriends.html", friends=friends)
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect("/friends")
        except:
            return "error updating"
    else: 
        return render_template("update.html", friend_to_update=friend_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_update = Friends.query.get_or_404(id)
    try:
            db.session.delete(friend_to_update)
            db.session.commit()
            return redirect("/friends")
    except: 
        return "There was a problem deleting"


if __name__ == "__main__":
    app.run()
