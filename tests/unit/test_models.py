from models.models import User
from werkzeug.security import generate_password_hash

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    email='fikret@test.com'
    username='fikret12'
    password1 ='testpassword'
    user =User(email=email,username=username,password=generate_password_hash(password1,method='sha256'))
    
    assert user.email ==email
    assert user.username == username
    assert user.password != password1