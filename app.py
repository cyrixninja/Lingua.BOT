# Importing Libraries
from flask import Flask, render_template, request, redirect , session, jsonify
import json
from jose import jwt
from requests.exceptions import HTTPError
from flask import url_for
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode
import base64
from os import urandom , environ as env
from urllib.parse import quote_plus
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import gen_quiz as genq
from bson import json_util
from bson.json_util import dumps
import json


# MongoDB Connection
# Create a MongoDB client
client = MongoClient('mongodb://localhost:27017')


# Connect to your database
db = client['LinguaBOT']

# Connect to your collection
notes_collection = db['notes']
quiz_collection = db['quiz']

# Loading the environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Creating a Flask app
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Configuration
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)



@app.route('/', methods=["GET",'POST'])
def index():
    if "user_info" in session:
        email = (session.get("user_info")['email'])
        print(email)
    return render_template('index.html', **locals())

@app.route('/genquiz', methods=["GET",'POST'])
def genquiz():
    if request.method == 'POST':
        language = request.form['language']
        difficulty = request.form['difficulty']
        email = session.get("user_info")['email']
        print(language, difficulty)
        quiz = genq.generate_quiz(language, difficulty)
        quiz['email'] = email 
        quiz['topic'] = (language+" "+difficulty)
        quiz_collection.insert_one(quiz)
        print(quiz)
        return redirect(url_for('quiz'))

@app.route('/chat', methods=["GET",'POST'])
def chat():
    if "user_info" not in session:
        return redirect(url_for("login"))
    else:
        email = (session.get("user_info")['email'])
        if request.method == 'POST':
            title = request.form['title']
            note = request.form['note']
            print(email, title, note)
            notes_collection.insert_one({'email': email, 'title': title, 'note': note})
    return render_template('chat.html', **locals())


@app.route('/cards', methods=["GET",'POST'])
def cards():
    if "user_info" not in session:
        return redirect(url_for("login"))
    else:
        email = session.get("user_info")['email']
        notes = list(notes_collection.find({'email': email}))
    return render_template('cards.html', **locals())

@app.route('/quiz', methods=["GET",'POST'])
def quiz():
    if "user_info" not in session:
        return redirect(url_for("login"))
    else:
        email = session.get("user_info")['email']
        topics = quiz_collection.distinct("topic", {"email": f"{email}"})
        quiz_data = quiz_collection.find({"email": f"{email}"})
        quiz_data = list(quiz_data)
        quiz_data = dumps(quiz_data)
        quiz_data = json.loads(quiz_data)
    return render_template('quiz.html', topics=topics, quizzes=quiz_data)

# Auth0 Authentication 

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    # Fetch user info
    resp = oauth.auth0.get(f"https://{env.get("AUTH0_DOMAIN")}/userinfo")
    user_info = resp.json()
    # Save user info into flask session
    session["user_info"] = user_info
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route('/delete_note/<note_id>', methods=['POST'])
def delete_note(note_id):
    notes = db['notes']  # Connect to your notes collection
    result = notes.delete_one({'_id': ObjectId(note_id)})  # Delete the note with the given id

    if result.deleted_count == 1:
        return {"success": True}, 200  # Return success status if the note was deleted
    else:
        return {"success": False}, 404  # Return failure status if no note was found with the given id
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)