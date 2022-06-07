
from flask import Flask, render_template, \
    redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, migrate
import sqlite3
import os
import psycopg2



# i set an env variable in powershell:
# $env:FLASK_APP = "webapp"

app = Flask(__name__)

DATABASE_URL = 'postgres://odmpmyvhuaasgq:b89b69c44e264196aaa2d9ba83b9539f6c877c5453da450c3aacedb127439393@ec2-52-30-67-143.eu-west-1.compute.amazonaws.com:5432/dfv12skb1ba9h'

# makes a configuration setting so we can use SQLite database in our app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///tasks.db')
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create SQLAlchemy database instance...just as easy as creating an object!
db= SQLAlchemy(app)


# migrate = Migrate(app,db)

all_items = []

# db Models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    done = db.Column(db.Boolean, unique=False, default=False, nullable=False)
    taskdes = db.Column(db.String(250), unique=False, nullable=False)

    # def __init__(self, done, taskdes):
    #     self.id = id
    #     self.done = False
    #     self.taskdes = taskdes
    # def __repr__(self):
    #     return f"Done? {self.done}, Task: {self.taskdes}"



@app.route("/")
def homepage():
    all_items = db.session.query(Item).all()
    return render_template("index.html", all_items=all_items)

@app.route("/submit", methods=["GET","POST"])
def add_task():
    if request.method == "POST":
        new_task = request.form.get("new_task_sent")
        new_item=Item(done=False, taskdes=new_task)
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for("homepage"))

@app.route("/update", methods=["GET","POST"])
def update_task():
    all_items = db.session.query(Item).all() # this is all db items before form updated
    if request.method == "POST":
        count = 0
        all_data = request.form # this is all the form data
        all_keys = all_data.keys()
        # for check_key in all_keys:
        #     print(f"check key is: {check_key}")
        print(f"all keys are: {all_keys}")
        print(all_data)
        to_delete = False
        # for thing in all_items:
        #     thing.done = False # turns all db entries False, we'll add True back in next step
        for check_key in all_keys:
            if check_key[:16] == "updateTaskButton":
                delete_item_number = int(check_key[16:])
                print(f"delete number is {delete_item_number}")
                delete_item = Item.query.get(delete_item_number)
                if delete_item.done == True:
                    to_delete = True # we'll delete at end

        for thing in all_items:
            thing.done = False # turns all db entries False, we'll add True back in next step

        for check_key in all_keys:
            if check_key[:15] == "update_checkbox":
                update_item_number = int(check_key[15:]) # returns all checkboxes that were checked
                update_item = Item.query.get(int(check_key[15:]))
                update_item.done = True
        if to_delete == True:
            db.session.delete(delete_item)
        db.session.commit()

        # for thing in all_items:
        #     id_label_now = "id_label" + str(count)
        #     # update_id = int(request.form.get(id_label_now))
        #     # print(f"update_id is {update_id}, type {type(update_id)}")
        #     update_item = Item.query.get(count)
        #     # print(f"checkbox says {request.form.get('update_checkbox')} of type {type(request.form.get('update_checkbox'))}")
        #     print(f"text says {request.form.get('update_text1')} of type {type(request.form.get('update_text1'))}")
        #     update_checkbox_now = "update_checkbox" + str(count)
        #     print(f"checkbox says {request.form.get('update_checkbox_now')} of type {type(request.form.get('update_checkbox_now'))}")
        #     print(f"checkbox now is: {update_checkbox_now}")
        #     if request.form.get(update_checkbox_now) == "on":
        #         print(f"thing.done should be on? it's {thing.done}")
        #         thing.done = True
        #     else:
        #         print(f"thing.done should be off? it's {thing.done}")
        #         thing.done = False
        #     # update_item.done = request.form.get("update_checkbox")
        #     count += 1
        # db.session.commit()
    return redirect(url_for("homepage"))


if __name__ == '__main__':
    app.run(debug=True)