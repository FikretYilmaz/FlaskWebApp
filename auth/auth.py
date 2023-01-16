
#*All the route related with authentication like login,sign up etc.

from flask import Blueprint,render_template,redirect,url_for,request,flash
from app import db
from models.models import User,Reactor
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os
import pandas as pd
from wtforms import MultipleFileField,SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired

auth = Blueprint('auth',__name__) #* Help us to Store different routes together

@auth.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email=request.form.get('email') #*Using get method help us with returning "null" if the data is not exist
        password=request.form.get('password') 
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is not correct',category='error')
        else:
            flash('Email does not exist',category='error')
    return render_template('login.html',user=current_user)


@auth.route('/sign-up',methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':        
        email=request.form.get('email') #*Using get method help us with returning "null" if the data is not exist
        user_name=request.form.get('username') 
        password1=request.form.get('password1') 
        password2=request.form.get('password2') 
        email_exists = User.query.filter_by(email = email).first()
        username_exists = User.query.filter_by(username = user_name).first()
        if email_exists:
            flash('Email is already in use',category='error')
        elif username_exists:
            flash('Username is already in use',category='error')
        elif password1 != password2:
            flash('Password does not match',category='error')
        elif len(user_name) < 2 :
            flash('Username is too short')
        elif len(password1) < 6 :
            flash('Password is too short')
        else:
            new_user = User(email=email,username=user_name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('User Created',category='success')
            return redirect(url_for('views.home'))
            
    return render_template('signup.html',user=current_user)


@auth.route('/logout')
@login_required #* You can only access this route you if you are login
def logout():
    logout_user()
    return redirect(url_for('views.home')) #*Redirect to user the home function in the vies.py


@auth.route('/upload',methods=['GET', 'POST'])
@login_required
def upload():
    ALLOWED_EXTENSION = set(['csv'])
    form=None
    class UploadFileForm(FlaskForm):
        files = MultipleFileField('File',validators=[InputRequired()])
        submit = SubmitField('Upload File')
    form = UploadFileForm() 
    def allowed_file(fileName):
        return '.' in fileName and fileName.rsplit('.', 1)[1] in ALLOWED_EXTENSION   #Check the file extension
    if form.validate_on_submit():
        for file in form.files.data:
            filename = secure_filename(file.filename)
            if allowed_file(file):
                df_local_af_mapping = pd.read_csv(file)
                df=pd.DataFrame()
                for index, row in df_local_af_mapping.iterrows():
                    TagName=[row['id'],row['combined_feed_H2'],row['combined_feed_CO']]
                    tagType=['id','combined_feed_H2','combined_feed_CO']
                    df2=pd.DataFrame({'Tagname':TagName, 'ReactorId':row['Reactor'],'tagType':tagType})
                    df=pd.concat([df,df2],ignore_index=True)
                df.to_sql(con=db.engine,name='reactor',index=False,if_exists='append')
                flash('CSV fil successfully added',category='success')
            else:
                flash(f'Not Supported File extension for {filename}. Only allowed to upload the CSV files',category='error')
        return render_template('upload.html',form=form,user=current_user)
    else:
        return render_template('upload.html',form=form,user=current_user)
    
@auth.route('/show',methods=['GET', 'POST'])
@login_required
def show():
    query2 =db.session.query(Reactor.ReactorId,Reactor.Tagname,Reactor.tagType).all()    
    return render_template('show_csv.html',queries=query2,user=current_user)

    