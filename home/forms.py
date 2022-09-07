from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, FileField, RadioField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from home.items import Item
import re

class Registerfield(FlaskForm):

    def validate_user(self, user_to_check):
        user = Item.query.filter_by(name=user_to_check.data).first()
        if user:
            raise ValidationError('USER ALREADY EXISTS')
        x = re.search(r"^[A-Z][A-Za-z0-9]+_[A-Z][A-Za-z0-9]+$", user_to_check.data)
        if not x:
            raise ValidationError('Name has to be in form of: Name_Hospital (First character in uppercase, Only alphanumirical values allowed)')

    user = StringField(label='Name_Company', validators=[Length(min=8, max=35), DataRequired()])
    email = EmailField(label='Email', validators=[Email(),DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=4, max=15), DataRequired()])
    password_confirmation = PasswordField(label='Confirmation password', validators=[EqualTo("password")])
    submit = SubmitField(label='Submit')

class Loginfield(FlaskForm):
    username = StringField(label=' User name', validators=[DataRequired()])
    password = PasswordField(label=' Password', validators=[DataRequired()])
    submit = SubmitField(label=' Log in')

class Uploadfield(FlaskForm):
    file = FileField(label='The medical image',validators=[DataRequired()])
    Method = RadioField(label='Methods', choices=[(1,'DCT'), (2,'LSB')],validators=[DataRequired()],coerce=int,default=1)
    submit = SubmitField(label='Watermark it')

class Extractfield(FlaskForm):
    file = FileField(label='The medical image',validators=[DataRequired()])
    hashkey = StringField(label='Your key',validators=[DataRequired()])
    Method = RadioField(label='Methods', choices=[(1, 'DCT'), (2, 'LSB')], validators=[DataRequired()], coerce=int,default=1)
    submit = SubmitField(label='Get msg')