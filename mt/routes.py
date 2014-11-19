from mt import app
from flask import Flask, render_template, request, flash, session, redirect, url_for, g, abort
from forms import SignupForm, SigninForm, TweetForm
from models import db, User, Message, Follower

@app.before_request
def before_request():
    g.user = None
    if 'uid' in session:
        g.user = db.session.query(User).filter(User.user_id == session['uid']).first()


@app.route('/')
def home():
    if 'uid' not in session:
        return redirect(url_for('public_timeline'))
    else:
        return redirect(url_for('user_timeline', uid=session['uid']))

@app.route('/public')
def public_timeline():
    return render_template('timeline.html',
        messages = db.session.query(Message, User).filter(Message.author_id == User.user_id).order_by(Message.pub_date.desc())
    )
    
@app.route('/<uid>')
def user_timeline(uid):
    user = db.session.query(User).filter(User.user_id == uid).first()
    if user is None:
        abort(404)
    else:
        followed = False
        if 'uid' in session:
            followed = True if db.session.query(Follower).filter(Follower.who_id == session['uid'], Follower.whom_id == uid).first() else False
        form = TweetForm()
        return render_template('timeline.html',
            messages = db.session.query(Message, User).filter(Message.author_id == User.user_id).filter(Message.author_id == uid).order_by(Message.pub_date.desc()),
            profile_user = user,
            form = form,
            followed = followed
        )

@app.route('/<uid>/follow')
def follow_user(uid):
    if 'uid' not in session:
        return redirect(url_for('home'))
    new_followed = Follower(session['uid'], uid)
    db.session.add(new_followed)
    db.session.commit()
    flash('You are now following this user')
    return redirect(url_for('user_timeline', uid=uid))

@app.route('/<uid>/unfollow')
def unfollow_user(uid):
    if 'uid' not in session:
        return redirect(url_for('home'))
    followed = db.session.query(Follower).filter(Follower.who_id == session['uid'], Follower.whom_id == uid).first()
    db.session.delete(followed)
    db.session.commit()
    flash('You are no longer following this user')
    return redirect(url_for('user_timeline', uid=uid))
    

@app.route('/add_tweet', methods=['POST'])
def add_tweet():
    form = TweetForm(request.form)    
    if request.method == "POST" and form.validate():
        new_tweet = Message(session['uid'], form.text.data)
        db.session.add(new_tweet)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
        
    

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
            user = db.session.query(User).filter(User.email == form.email.data).first()
            session['uid'] = user.user_id
            return redirect(url_for('user_timeline', uid=session['uid']))
    
    elif request.method == 'GET':
        return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
  if 'uid' not in session:
    return redirect(url_for('signin'))
     
  session.pop('uid', None)
  return redirect(url_for('home'))

        
    
    
        
    


    