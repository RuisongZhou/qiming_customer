from app import app
from flask import render_template,request
from app.sockets import *
import json
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", name="index")


@app.route('/send', methods=['POST'])
def result():
    if request.method == "POST":
        question = request.form['question']
        answer = send_question(question)
        print(answer)
        return answer