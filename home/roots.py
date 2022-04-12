from home import app
from flask import request, render_template


@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def hello_world():  # put application's code here
    return render_template("index.html")

@app.route('/researchs')
def mainpage():
    return render_template("recherches.html")
@app.route('/Types')
def types():
    return render_template("Types.html")

@app.route('/AI')
def aipage():
    return render_template("AI.html")

@app.route('/Contact')
def contract_page():
    return render_template("Contact.html")