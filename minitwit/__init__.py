from flask import Flask

app = Flask(__name__)

app.secret_key = 'manutd'

SQLALCHEMY_DATABASE_URI = 'mysql://root:6868@localhost/self'

app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

from models import db
db.init_app(app)

import minitwit.routes
