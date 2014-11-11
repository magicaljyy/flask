from minitwit import app
from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import ContactForm, SignupForm, SigninForm
from models import db, User

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    
    if request.method=='POST':
        if form.validate() == False:
            return render_template('signup.html', form = form)
        else:
            new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = new_user.email
            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
            
            
    elif request.method == 'GET':
        return render_template('signup.html', form=form)