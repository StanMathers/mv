from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Registration(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50), Email()])
	name = StringField('Name', validators=[DataRequired(), Length(min=5, max=50)])
	surname = StringField('Surname', validators=[DataRequired(), Length(min=5, max=50)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
	submit = SubmitField('Register')



class Login(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(min=5, max=50), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])
	submit = SubmitField('Login')


class CommentField(FlaskForm):
	comment_written = TextAreaField('Comment', validators=[DataRequired(), Length(min=5, max=500)])
	submit = SubmitField('Comment')

