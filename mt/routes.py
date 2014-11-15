from mt import app
from flask import Flask, render_template, request, flash, session, redirect, url_for
from forms import SignupForm, SigninForm, TweetForm
from models import db, User, Message

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/public')
def public_timeline():
    return render_template('timeline.html',
        messages = db.session.query(Message, User).filter(Message.author_id == User.user_id).all())
    
@app.route('/<uid>')
def user_timeline(uid):
    if 'uid' not in session:
        return redirect(url_for('public_timeline'))
    user = User.query.filter_by(user_id = uid).first()
    
    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('timeline.html',
            messages = db.session.query(Message, User).filter(Message.author_id == User.user_id).filter(Message.author_id == uid).all(),
            profile_user = user
        )

@app.route('/add_tweet', methods=['POST'])
def add_tweet():
    if 'uid' not in session:
        return redirect(url_for('public_timeline'))
    
    form = TweetForm()
    if form.validate() == False:
        return redirect(url_for('user_timeline', session['uid']))
        
    new_tweet = Message(uid, form.text.data)
    db.session.add(new_tweet)
    db.session.commit()
    return redirect(url_for('timeline'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form = form)
        else:
            new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            session['uid'] = new_user.user_id
            return redirect(url_for('user_timeline', uid = session['uid']))
            
            
    elif request.method == 'GET':
        return render_template('signup.html', form = form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signin.html', form = form)
        else:
            user = db.session.query(User).filter(User.email == session['email']).first()
            session['uid'] = user.user_id
            return redirect(url_for('user_timeline', uid=session['uid']))
    
    elif request.method == 'GET':
        return render_template('signin.html', form=form)

        
    
    
        
    


    