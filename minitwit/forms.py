from wtforms import Form, TextField, SubmitField, validators, ValidationError, PasswordField
from models import db, User

class SignupForm(Form):
    first_name = TextField('First Name', [validators.length(min = 1, max = 15)])
    last_name = TextField('Last Name', [validators.length(min = 1, max = 15)])
    email = TextField("Email",  [
        validators.Required('Please enter your email address.'),
        validators.Email('Please enter your email address.')
    ])
    password = PasswordField('Password', [
        validators.Required('Please enter'),
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
    
    