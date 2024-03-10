# Importing Libraries
from flask import Flask, render_template, request, redirect , session
import json


# Creating a Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=["GET",'POST'])
def index():
    print("Hello World !")
    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)