from flask import Flask
from flask.ext.admin import Admin

app = Flask(__name__)
app.config.from_object('config')

admin = Admin(app, name='online-judge', template_mode='bootstrap3')

import views
import controllers
