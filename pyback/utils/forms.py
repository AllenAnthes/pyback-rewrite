from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, BooleanField


class CodeSchoolForm(FlaskForm):
    name = StringField('School Name', [validators.required()])
    url = StringField('School website url', [validators.required()])
    fulltime = BooleanField('Fulltime available?')
    hardware = BooleanField('Hardware included?')
    has_online = BooleanField('Online Offered?')
    only_online = BooleanField('Only online?')
    accredited = BooleanField('VA Accredited?')

    rep_name = StringField('School Representative', [validators.required()])
    rep_email = StringField('Representative Email', [validators.required()])
    address1 = StringField('Address Line 1', [validators.required()])
    address2 = StringField('Address Line 2', [validators.required()])
    city = StringField('City', [validators.required()])
    state = StringField('State', [validators.required()])
    zipcode = StringField('Zipcode', [validators.required()])
    country = StringField('Country', [validators.required()])

    logo = FileField(validators=[FileAllowed(['jpg', 'png'], 'Images only')])

    recaptcha = RecaptchaField()


