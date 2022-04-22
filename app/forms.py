from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,TextAreaField,IntegerField,SelectField,DateField
from wtforms.validators import DataRequired,Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone=StringField('phone',validators=[DataRequired()])
    submit = SubmitField('register')

class AddStore(FlaskForm):
    name=StringField('name',validators=[DataRequired()])
    location=StringField('location',validators=[DataRequired()])
    submit = SubmitField('Add')
class AddProduct(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    model=StringField('model',validators=[DataRequired()])
    serial=StringField('serial',validators=[DataRequired()])
    price=StringField('price',validators=[DataRequired()])
    quantity=StringField('quantity',validators=[DataRequired()])
    submit=SubmitField("add")

class Search(FlaskForm):
    date=DateField('date')
