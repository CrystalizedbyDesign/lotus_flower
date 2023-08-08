from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import Sign_up 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re 


@app.route('/') 
def index():
    return render_template('login.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    
    # Handle GET request to display the sign-up form
    if request.method == 'GET':
        return render_template('sign_up.html')
    
    
    elif request.method == 'POST':
        # Handle POST request for form submission and user registration
        if not Sign_up.validate_sign_up(request.form):
            return redirect('/')

    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "username": request.form['username'],
        "age": request.form['age'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    # Save the data without storing the result
    id = Sign_up.save(data)
    # Rest of the code remains the same
    session['user_id'] = id
    return redirect('/dashboard')


@app.route('/login', methods=['GET','POST'])
def login():
    # see if the username provided exists in the database
    
    user_in_db = Sign_up.get_by_email(request.form)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if not 'user_id'  in session:
        return redirect ('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('affirmations.html', user_in_db=Sign_up.get_by_login_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

