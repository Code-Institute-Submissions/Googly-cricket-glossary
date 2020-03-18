import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "Googly"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

@app.route("/")
def index():
    return render_template('index.html', letters=alphabet)
    

@app.route("/display_letter/<letter>")
def display_letter(letter):
    return render_template("letter.html",
                           letter=mongo.db.entries.find({
                            "letter": letter}).sort("term"), letters=alphabet)

@app.route("/display_word/<word>")
def display_word(word):
    return render_template("word.html",
                           word=mongo.db.entries.find_one({
                            "term": word}), letters=alphabet)


@app.route("/add_word")
def add_word():
    return render_template("addword.html", letters=alphabet)


@app.route("/insert_word", methods=["GET", "POST"])
def insert_word():
    word = request.form["term"]
    entries = mongo.db.entries
    all_entries = mongo.db.entries.find()
    glossary = [entry["term"] for entry in all_entries]

    if word not in glossary:
        entries.insert_one(
        {
            "term": word,
            "letter": word[0].upper(),
            "meanings": [request.form["meaning1"], 
                        request.form["meaning2"], 
                        request.form["meaning3"]]
        })
        flash("Word successfully added.")
        return redirect(url_for("display_word", word=word))
    else:
        flash(("Entry '{}' already exists.").format(word))
        return redirect(url_for("add_word"))
        
        

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
