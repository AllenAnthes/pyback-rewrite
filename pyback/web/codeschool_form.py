from os import path, remove
from typing import Tuple
from urllib import parse

import requests
from flask import json, jsonify, current_app, request, after_this_request, send_file
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from werkzeug.datastructures import FileStorage
from werkzeug.local import LocalProxy
from werkzeug.utils import secure_filename
from wtforms import StringField, validators, BooleanField

logger = LocalProxy(lambda: current_app.logger)


class CodeSchoolForm(FlaskForm):
    name = StringField('School Name', [validators.required()])
    url = StringField('School website url', [validators.required()])
    fulltime = BooleanField('Fulltime available?')
    hardware = BooleanField('Hardware included?')
    has_online = BooleanField('Online Offered?')
    only_online = BooleanField('Online only?')
    accredited = BooleanField('VA Accredited?')
    housing = BooleanField('Housing Included?')
    mooc = BooleanField('MOOC Only?')

    rep_name = StringField('School Representative', [validators.required()])
    rep_email = StringField('Representative Email', [validators.required()])
    address1 = StringField('Address Line 1', [validators.required()])
    address2 = StringField('Address Line 2')
    city = StringField('City', [validators.required()])
    state = StringField('State', [validators.required()])
    zipcode = StringField('Zipcode', [validators.required()])
    country = StringField('Country', [validators.required()])

    logo = FileField(validators=[FileAllowed(['jpg', 'png'], 'Images only')])

    recaptcha = RecaptchaField()


def handle_submission(form: CodeSchoolForm):
    save_logo(form.logo.data)
    repo_path = current_app.config['GITHUB_REPO_PATH']
    url = f"https://api.github.com/repos/{repo_path}/issues"
    headers = {"Authorization": f"Bearer {current_app.config['GITHUB_JWT']}"}

    params = make_params(**form.data)
    res = requests.post(url, headers=headers, data=json.dumps(params))

    if res.ok:
        return jsonify({'redirect': f'https://github.com/{repo_path}/issues'})
    else:
        return res.reason


def save_logo(file: FileStorage) -> None:
    filename = secure_filename(file.filename)
    filepath = path.join(current_app.static_folder, 'logos', filename)
    file.save(filepath)


def get_logo_and_users(logo: FileStorage) -> Tuple[str, str]:
    school_logo = parse.quote(secure_filename(logo.filename))
    if current_app.config['ENV'] == 'development':
        users = '@wimo7083 @AllenAnthes,'
        # users = '@AllenAnthes,'
        logo_url = f'https://pybot.ngrok.io/static/logos/{school_logo}'
        return logo_url, users
    else:
        url_root = request.url_root
        # users = '@hpjaj @wimo7083 @jhampton @kylemh @davidmolina @nellshamrell @hollomancer @maggi-oc'
        users = ''
        logo_url = f'{url_root}static/logos/{school_logo}'
        return logo_url, users


def get_logo(filename):
    """
    Currently unused.  Attempting to just serve logo as a static asset
    """
    filepath = path.join(current_app.static_folder, 'logos', filename)
    file_handle = open(path.normpath(filepath), 'r')

    @after_this_request
    def remove_file(response):
        try:
            remove(filepath)
            file_handle.close()
        except Exception as error:
            logger.exception("Error removing or closing downloaded file handle", error)
        return response

    return send_file(filepath)


def make_params(logo, name, url, address1, city, state, zipcode, country, rep_name, rep_email, csrf_token, recaptcha,
                address2=None, fulltime=False, hardware=False, has_online=False, only_online=False, accredited=False,
                housing=False, mooc=False):
    logo_url, notify_users = get_logo_and_users(logo)

    return ({
        'title': f'New Code School Request: {name}',
        'body': (
            f"Name: {name}\n"
            f"Website: {url}\n"
            f"Full Time: {fulltime}\n"
            f"Hardware Included: {hardware}\n"
            f"Has Online: {has_online}\n"
            f"Only Online: {only_online}\n"
            f"VA Accredited: {accredited}\n"
            f"Housing Included: {housing}\n"
            f"MOOC Only: {mooc}\n"

            f"Address: {address1} {address2}\n"
            f"City: {city}\n"
            f"State: {state}\n"
            f"Country: {country}\n"
            f"Zip: {zipcode}\n\n"
            f"Representative Name: {rep_name}\n"
            f"Representative Email: {rep_email}\n"

            f"logo: ![school-logo]({logo_url})\n"

            'This code school is ready to be added/updated:\n'
            f"{notify_users}\n"
            "Please close this issue once you've added/updated the code school."
        )
    })
