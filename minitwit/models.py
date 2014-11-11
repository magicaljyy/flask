from flask.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    pw_hash = db.Column(db.String(255))
    
    def __init__(self, firstname, lastname, email, password):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)
        
    def __repr__(self):
        return '<User %r>' % self.username
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

class Follower(db.Model):
    __tablename__ = 'follower'
    
    who_id = db.Column(db.Integer)
    whom_id = db.Column(db.Integer)
    
    def __init__(self, who_id, whom_id):
        self.who_id = who_id
        self.whom_id = whom_id

    def __repr__(self):
        return '<User %d is following %d>'.format(self.who_id, self.whom_id)
    
class Message(db.Model):
    __tablename__ = 'message'
    
    message_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    author_id = db.Column(db.Integer)
    text = db.Column(db.String(255))
    
    def __init__(self, author_id, text):
        self.author_id = author_id
        self.text = text
        
    def __repr__(self):
        '<User %d just post %s>'.format(self.author_id, self.text)

    
