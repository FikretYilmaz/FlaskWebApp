from dotenv import load_dotenv,find_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
import pyodbc
import urllib
from sqlalchemy import create_engine
load_dotenv(find_dotenv())
# #*Creating DB with SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)

my_secret_key = os.getenv("SECRET_KEY")
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_SERVER=os.getenv('DB_SERVER')
DB_NAME=os.getenv('DB_NAME')
# DB_PORT=os.getenv('DB_PORT')
DRIVER= os.getenv('DRIVER')

# POSTGRES=os.getenv('POSTGRES')

params = urllib.parse.quote_plus(
    'Driver=%s;' % DRIVER +
    'Server=tcp:%s,1433;' % DB_SERVER +
    'Database=%s;' % DB_NAME +
    'Uid=%s;' % DB_USER +
    'Pwd={%s};' % DB_PASSWORD +
    'Encrypt=yes;' +
    'TrustServerCertificate=no;' +
    'Connection Timeout=30;')

conn_str = 'mssql+pyodbc:///?odbc_connect=' + params

#*Initialize DB
# app.config['SQLALCHEMY_DATABASE_URI']=f'mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_DATABASE_URI']=conn_str

# app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES
app.config['SECRET_KEY'] = my_secret_key
db.init_app(app)
migrate = Migrate(app, db)

from views import views
from auth import auth

app.register_blueprint(views, url_prefix="/") #* We are registering our blueprint to our flask app
app.register_blueprint(auth, url_prefix="/")

#* Before we create DB we call all of models
from models import User  

#* Check the user is login or not if not redirect user to the page we want
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ =='__main__':
    app.run()