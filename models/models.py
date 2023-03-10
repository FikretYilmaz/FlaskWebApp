from app import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin): #* Inherit from base class =>db.Model 
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    username = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    public_id = db.Column(db.String(50), unique=True)
    
class Reactor(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Tagname = db.Column(db.String(150))
    ReactorId = db.Column(db.String(150))
    tagType = db.Column(db.String(150))
    
    