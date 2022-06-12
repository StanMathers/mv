from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Registration(FlaskForm):
	email = StringField('Email', validators=[DataRequired('Please, enter an email'), Length(min=5, max=50), Email()])
	name = StringField('Name', validators=[DataRequired('Please, enter your name'), Length(min=5, max=50)])
	surname = StringField('Surname', validators=[DataRequired('Please, enter your surname'), Length(min=5, max=50)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
	confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo(password)])
	submit = SubmitField('Register')




class Login(FlaskForm):
	pass


class Comment(FlaskForm):
	pass

