from flask import Flask
from flask import render_template, request, redirect, url_for, send_from_directory, session
import pyrebase
import datetime
import findprice
import download
import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("/Users/carlosborjes/Desktop/real-rustoleum/rustoleumauth-firebase-adminsdk-xboy0-0991945e03.json")
firebase = pyrebase.initialize_app(config)
auth=firebase.auth()

app = Flask(__name__)
@app.route("/")
def hello_there():
    return redirect(url_for("login"))

@app.route("/login", methods =["GET", "POST"])
def login():
    # link_clicked = request.args.get('link_clicked')
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        try:
            user=auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for("search")) 
        except:
            return redirect(url_for("login"))
    return render_template("rustoleum_login.html")

@app.route("/signup", methods =["GET", "POST"])
def signup():
    if request.method == "POST":
        email=request.form.get("email")
        password=request.form.get("password")
        try:
            user=auth.create_user_with_email_and_password(email,password)
            auth.send_email_verification(email)
            return redirect(url_for("login"))
        except:
            return redirect(url_for("signup"))
    return render_template(
        "signup.html"
    )

@app.route("/forgotpassword",methods =["GET", "POST"])
def forgotpass():
    if request.method == "POST":
        email=request.form.get("email")
        auth.send_password_reset_email(email)
        return redirect(url_for("login"))
    return render_template(
        "rustforgotpass.html"
    )

@app.route("/search", methods =["GET", "POST"])
def search():
    if request.method == "POST": 
        item_num = request.form.get("search")
        x=findprice.scrapelowes(item_num)
        y=findprice.scrapedepot(item_num)
        z=findprice.scrapeace(item_num)
        download.addtofile(x,y,z,item_num)
        return render_template("displayitemprice.html",lowesvalue=x,itemnum=item_num,homedepotvalue=y,acevalue=z)
    return render_template("displayitemprice.html")

    
@app.route("/<path:path>")
def static_file(path):
    return send_from_directory("",path)

if __name__ == "__main__":
    app.run(debug=True)
    
