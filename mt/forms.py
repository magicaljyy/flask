from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, validators, ValidationError, PasswordField
from models import db, User

class SignupForm(Form):
    first_name = TextField('First Name', [validators.length(min = 1, max = 15)])
    last_name = TextField('Last Name', [validators.length(min = 1, max = 15)])
    email = TextField("Email",  [
        validators.Required('Please enter your email address.'),
        validators.Email('Please enter your email address.')
    ])
    password = PasswordField('Password', [
        validators.Required('Please enter a password'),
        validators.EqualTo('confirm', message = 'Password must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Create account")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        if not Form.validate(self):
          return False
     
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
          self.email.errors.append("That email is already taken")
          return False
        else:
          return True
          
class SigninForm(Form):
    email = TextField('Email', [validators.Required('Please enter your email address')])
    password = PasswordField('Password', [validators.Required('Please enter a password')])
    
    submit = SubmitField('Sign In')
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
    
    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append('Invalid login details')
            return False

class TweetForm(Form):
    text = TextField('Tweet', [validators.Required('Pleas enter your Tweet')])
    submit = SubmitField('Submit')
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        