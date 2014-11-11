from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'mysql://root:6868@localhost/self'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
db = SQLAlchemy(app)
        
@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'
    
if __name__ == '__main__':
    app.run()
