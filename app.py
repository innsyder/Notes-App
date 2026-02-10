# Imports
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime 

# MY APP 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db = SQLAlchemy (app)
Scss(app, static_dir="static", asset_dir="assets")

class Note(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    text = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def home():
    all_notes = Note.query.order_by(Note.date).all()
    return render_template("index.html", notes=all_notes)
    

@app.route("/add", methods=["POST"])
def add_note():
    note_text = request.form["note"]                   #get the text from the form 
    new_note = Note(text=note_text)
    db.session.add(new_note)
    db.session.commit()                                #add it to our list
    return redirect("/")                               #go back to the homepage 

@app.route("/delete/<int:id>", methods=["POST"])
def delete_note(id):
    note_to_delete = Note.query.get_or_404(id)
    db.session.delete(note_to_delete)
    db.session.commit()   
    return redirect("/")

@app.route("/edit/<int:id>")
def edit_page(id):
    note = Note.query.get_or_404(id)
    return render_template("edit.html", note=note)
    

@app.route("/update/<int:id>", methods=["POST"])
def update_page(id):
    note = Note.query.get_or_404(id)
    new_text = request.form["new_text"]
    note.text = new_text
    db.session.commit()
    return redirect("/")

if __name__ in "__main__":
    app.run(debug=True)
