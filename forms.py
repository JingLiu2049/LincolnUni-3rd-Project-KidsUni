from re import L
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# class UpdateAccountForm(FlaskForm):
#     first_name = StringField('First Name', validators=[DataRequired()])
#     surname = StringField('Surname', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     phone_number = IntegerField('Phone Number', validators=[DataRequired()])

class UpdatePassword(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')