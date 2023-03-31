from flask import Flask, flash, render_template, request,redirect
import socket
import re
import pandas as pd
import csv
import datetime


df = pd.read_csv("users.csv")
app=Flask(__name__)
app.secret_key = "heywizy"
hostname= socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

@app.route("/", methods = ["GET","POST"] )
def signin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        df = pd.read_csv("users.csv") 
        group = df.groupby("username")         
        if username  in df.values:   
            ok = group.get_group(username)
            if password in ok.values:
                return render_template("index.html", name = ok.iloc[0,1])
            else:
                flash ("Incorrect password or username!!!")       
        else:
                flash ("Incorrect password or username!!!")
    return render_template("auth-signin-basic.html")

@app.route("/signup", methods = ["GET","POST"] )
def signup():
    if request.method == "POST":
        useremail = request.form['useremail']
        username = request.form['username']
        password = request.form['password']
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        user_input = ['useremail','username','password']
        if useremail in df.values:
                flash("Account already exists!!", "error")
        elif username in df.values:
             flash("Account already exists!!", "error")

        else:    
            with open('users.csv','a',newline="") as inFile:
                writer = csv.DictWriter(inFile, fieldnames=user_input)
                writer.writerow({'useremail':useremail,'username': username ,'password':password})

                flash("Account has been successfully created!", "success")
                return redirect ("/")

    return render_template("auth-signup-basic.html")

@app.route("/signin", methods = ["GET","POST"])
def sin():
     return redirect("/")

@app.route("/index", methods = ["GET","POST"])
def index():
     return render_template("index.html")


if __name__=="__main__":
     app.run(host=str(IPAddr) , port =80, debug=True, threaded=True)