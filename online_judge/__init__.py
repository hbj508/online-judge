from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.admin import Admin
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
Bootstrap(app)
app.config.from_object('config')

admin = Admin(app, name='CodePro', template_mode='bootstrap3')

import views
import controllers
