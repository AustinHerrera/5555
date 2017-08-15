
import os
from flask import render_template, redirect, request, url_for, flash, session, g
import pandas as pd
from .Custom_functions import *
from .models import *
from app import app, db, lm
from flask_wtf import FlaskForm
from sqlalchemy.orm import sessionmaker
from .forms import LoginForm, SignupForm
from flask_login import login_user, current_user, login_required, logout_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .admin import AdminView
from .missingImages import * 
admin = Admin(app, name='Dashboard')
admin.add_view(ModelView(User, db.session))


def getMachines(ip):
    ip=ip
    user = 'RptSvc'
    password = 'utsreports'
    connx = dbconnect(ip, user, password)
    query = open(os.path.join('./app/queries/', 'get-machines.txt')).read()
    machines = dbquery(connx, query)
    return machines

def generateList():
    collection = machine.query.filter_by(Machinetypeid='2').all()
    machine_list = [a for a in collection]
    return machine_list

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        dbip = request.form["dbip"]
        session['contract'] = dbip
        return redirect(url_for('machines'))
    elif request.method == 'GET':
        return render_template("index.html",
                            title='Database selector',
                            server_list = generateList() )
#    return index
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/machines' , methods=['GET','POST'])
def machines():
    dbip  = session['contract'] 
    machines = getMachines(dbip)
    return render_template('machines.html', machines=[machines.to_html()])
    return machines

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            emailAddress = request.form.get("email")
            user= User.query.filter_by(email = emailAddress).first()
            if user:
                if user.verify_password(form.password.data):
                # if user.password == form.password.data:
                    loginUser = User(form.email.data, form.password.data)
                    login_user(loginUser)
                    return redirect(url_for('index'))
                    return "user Logged in"
                else:
                    return "Wrong password"
            else:
               return "User doesn't exist"
        else:
           return "form not validated"

@app.route("/logout")
def logout():
    logout_user()
    return index()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            emailAddress = form.email.data
            if User.query.filter_by(email = emailAddress).all():
                return "Email address already exists"
            else:
                newuser= User(form.email.data, form.password.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                return "User Created!!"
        else:
            return "Form didn't Validate"



@app.route('/missingImages', methods=['GET', 'POST'])
@login_required
def missingImages():
    contract = session['contract']
    missingImages =  MissingImages(contract)
    return render_template( "missingImages.html",  missingImages = missingImages.to_html())

@app.route('/flushedTags', methods=['GET', 'POST'])
@login_required
def flushedTagsView():
    contract = session['contract']
    flushedTagsresults = flushedTags(contract)
    return render_template("flushedTags.html", flushedTagsResults=flushedTagsresults.to_html(index=False))

@app.route('/AutoClosedWO', methods=['GET'])
@login_required
def AutoClosedWO():
	contract = session['contract']
	autoClosedResults = autoClosed(contract)
	return autoClosedResults
	

if __name__ == "__main__":
    secret_key = 'swordfish'
    app.run(debug=True)


