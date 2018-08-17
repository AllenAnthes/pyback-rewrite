from flask import url_for, redirect, render_template, logging
from datetime import datetime, timedelta
from itertools import chain
import os

from pyback.database.models import TemporaryUrl, User
from pyback import db, app

logger = app.logger


def get_temporary_url(user_id: str, text: str) -> TemporaryUrl:
    url = TemporaryUrl.query.filter_by(slack_user=user_id).first()
    if url and datetime.now() - url.created_on > timedelta(minutes=5):
        logger.info("URL expired before being used.  Making new one")
        db.session.delete(url)
        db.session.commit()
        url = None
    if not url:
        url = TemporaryUrl(slack_user=user_id)
        if text == 'debug':
            url.level = 'debug'
        else:
            url.level = 'info'
        db.session.add(url)
        db.session.commit()
        url = TemporaryUrl.query.filter_by(slack_user=user_id).first()
    return url


def verify_user(variable: str):
    url = TemporaryUrl.query.filter_by(url=variable).first()
    if not url:
        return redirect(url_for('HTTP403'))
    if datetime.now() - timedelta(minutes=5) > url.created_on:
        db.session.delete(url)
        logger.warning(f'Expired log requested from user id {url.slack_user}')
        return redirect(url_for('HTTP410'))  # Change this to a custom page

    db.session.delete(url)
    db.session.commit()
    return url.level


def get_logs(level):
    f = open(f'logs/{level}.log')
    lines = reversed(f.readlines())
    if os.path.isfile(f'logs/{level}.log.1'):
        f = open(f'logs/{level}.log.1')
        lines = chain(lines, reversed(f.readlines()))

    return lines


def can_view_logs(user_id: str):
    return bool(User.query.filter_by(slack_id=user_id, access_logs=True).first())
