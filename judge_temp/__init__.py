from flask import Flask
from flask.ext.admin import Admin
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')

admin = Admin(app, name='online-judge', template_mode='bootstrap3')

import views
import controllers
