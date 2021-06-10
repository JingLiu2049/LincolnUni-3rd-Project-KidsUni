import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class AddUser(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    user_access = SelectField('User Access', validators=[DataRequired(),], 
                                choices=[('restricted', 'Restricted'), ('admin', 'Admin')])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        # Check if the email already exists
        cur = db.getCursor()
        cur.execute('SELECT * FROM authorisation WHERE username = %s', (email.data,))
        user = cur.fetchone()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class UpdatePassword(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')