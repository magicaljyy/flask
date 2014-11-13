from mt import app
from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import SignupForm
from models import db, User, Message

@app.route('/')
def home():
  return render_template('home.html')

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
            return redirect(url_for('%s'.format(new_user.user_id)))
            
            
    elif request.method == 'GET':
        return render_template('signup.html', form = form)

@app.route('/signin')
def signin():
    print('jyy')
    about(404)

@app.route('/<uid>')
def user_timeline(uid):
    if 'email' not in session:
        return redirect(url_for('signin'))
    user = User.query.filter_by(user_id = uid).first()
    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('timeline.html',
            messages = Message.query.join(User, User.user_id == Message.author_id, User.user_id == uid).all(),
            profile_user = user
        )       

    