from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from bambiv3.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20), Regexp(r'^[\w.-_.]+$', message='No Spaces. Use "-" , "_" , "." instead') ])
	email = StringField('Email', validators = [DataRequired(), Email()])
	department = StringField('Department', validators=[DataRequired()])
	student_number = StringField('Student Number', validators=[DataRequired()])
	country = StringField('Country', validators=[DataRequired()])
	age = StringField('Age', validators=[DataRequired()])
	hobby = StringField('Hobby', validators=[DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is taken. Please choose a different one')

	def validate_student_number(self, student_number):
		user = User.query.filter_by(student_number=student_number.data).first()
		if user:
			raise ValidationError('That Student Number is taken. Please choose a different one')


class LoginForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()]) #Email()
	password = PasswordField('Password', validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20), Regexp(r'^[\w.-_.]+$')])
	email = StringField('Email', validators = [DataRequired(), Email()])
	picture = FileField('', validators=[FileAllowed(['jpg', 'jpeg' , 'png'])])
	department = StringField('Department', validators=[DataRequired()])
	student_number = StringField('Student Number', validators=[DataRequired()])
	country = StringField('Country', validators=[DataRequired()])
	age = StringField('Age', validators=[DataRequired()])
	hobby = StringField('Hobby', validators=[DataRequired()])
	bio = TextAreaField('Bio')
	private = BooleanField('Private?')
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one')


class PostForm(FlaskForm):
	title = StringField('Title') #validators=[DataRequired()]
	content = TextAreaField('Content', validators=[DataRequired()])
	image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg' , 'png', 'gif'])])
	submit = SubmitField('🛫 Post')

class MessageForm(FlaskForm):
    message = TextAreaField(('Message'), validators=[DataRequired()]) #Length(min=0, max=140)
    submit = SubmitField('send')

class ProductForm(FlaskForm):
	title = StringField(validators=[DataRequired()])
	description = TextAreaField(validators=[DataRequired()])
	location = StringField(validators=[DataRequired()])
	price = StringField(validators=[DataRequired()])
	contact = StringField(validators=[DataRequired()])
	image1 = FileField(validators=[FileAllowed(['jpg', 'jpeg' , 'png', 'gif']), DataRequired()])
	#image2 = FileField(validators=[FileAllowed(['jpg', 'jpeg' , 'png', 'gif'])])
	#image3 = FileField(validators=[FileAllowed(['jpg', 'jpeg' , 'png', 'gif'])])
	submit = SubmitField('🛫 Post')

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')
