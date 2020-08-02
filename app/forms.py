from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, DateField, RadioField, IntegerField
from wtforms.validators import InputRequired, Email, ValidationError

from app.models import User


class TripForm(FlaskForm):
    from_ = StringField('From')
    to_ = StringField('To')
    departure_date = DateField('Departure Date', format='%Y-%m-%d')
    trip_type = RadioField('Trip Type', choices=['One Way'], default='One Way')
    submit = SubmitField('Next')


class DriverDetailsForm(FlaskForm):
    driver_name = StringField('Driver Name', validators=[InputRequired('Please select the driver')])
    language = StringField('Language', validators=[InputRequired('Please select the driver')])
    car_name = StringField('Car', validators=[InputRequired('Please select the car')])
    submit = SubmitField('Next')


class BookingForm(FlaskForm):
    pickup_address = StringField('Pick Up Address', validators=[InputRequired('Please Enter the pickup address')])
    pickup_time = StringField('Pick Up Time', validators=[InputRequired('Select Pick up time')])
    submit = SubmitField('Next')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message='Username field is required.')])
    phone_number = IntegerField('Phone Number', validators=[InputRequired(message='Enter the phone number')])
    email = StringField("Email", validators=[InputRequired(message='Email field is required.'), Email()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message='Username field is required.')])
    email = StringField("Email", validators=[InputRequired(message='Email field is required.'), Email()])
    phone_number = IntegerField('Phone Number', validators=[InputRequired(message='Enter the phone number')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.get_user_by_username(username=username.data)
        if user is not None:
            raise ValidationError("User already exists")

    def validate_email(self, email):
        user = User.get_user_by_email(email=email.data)
        if user is not None:
            raise ValidationError("Email Id already exists try to login")
