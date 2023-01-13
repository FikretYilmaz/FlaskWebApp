#*All the views related with program
from flask import Blueprint,render_template
from flask_login import login_required,current_user

views = Blueprint('views',__name__) #* Help us to Store different routes together

@views.route('/') #*Put this two end points or route whenever user come to "/" or '/home' flask will return the same html
@views.route('/home')
@login_required
def home():
    return render_template('home.html',user=current_user)


