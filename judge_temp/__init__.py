from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from judge_temp import views
from judge_temp import controllers
