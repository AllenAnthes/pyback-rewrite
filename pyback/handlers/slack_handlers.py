import logging

from pyback.external.airtable_client import Airtable
from pyback.utils.action_menu_messages import suggestion_modal, action_menu_message
from pyback.utils.greeting_messages import *
from pyback.external.slack_client import Slack
from pyback import app
from pyback.utils.mentor_request_messages import mentee_claimed, mentee_unclaimed, base_claim_message

logger = logging.getLogger(__name__)


def new_member(user, **other):
    user_id = user['id']
    real_name = Slack.user_name_from_id(user_id)

    user_messages = make_greeting_messages(real_name)
    community_message = new_member_community_announcement(real_name)

    for message in user_messages:
        Slack.post_message(user_id, message, as_user=True)

    Slack.post_message(app.config['COMMUNITY_CHANNEL'], community_message)


def member_greeted(user, actions, original_message, channel, message_ts, **other):
    user_id = user['id']
    updated_button = greet_button_template(original_message, channel, message_ts)
    click_type = actions[0]['value']

    if click_type == 'greeted':
        updated_button['attachments'] = greeted_response(user_id)
    else:
        updated_button['attachments'] = not_greeted_response()

        if click_type == 'reset_greet':
            updated_button['attachments'][0]['text'] = reset_greet_message(user_id)

    Slack.update_message(**updated_button)


def action_menu(actions, channel, message_ts, **other):
    """
    Handles the interactive message sent to a new user when
    they first join
    """
    action_button = actions[0]['name']
    updated_message = action_menu_message(action_button, channel, message_ts)
    Slack.update_message(**updated_message)


def suggestion(trigger_id, **rest):
    dialog = suggestion_modal(trigger_id)
    Slack.open_dialog(**dialog)


def claim_mentee(user, actions, original_message, channel, message_ts, **rest):
    clicker_id = user['id']
    click_type = actions[0]['value']
    request_record = actions[0]['name']
    user_info = Slack.user_info_from_id(clicker_id)
    clicker_email = user_info['user']['profile']['email']
    message = base_claim_message(original_message, channel['id'], message_ts)

    attachment, mentor_id = get_response(click_type, clicker_id, clicker_email, original_message, request_record)

    message['attachments'] = attachment
    Slack.update_message(**message)

    Airtable.update_request(request_record, mentor_id)


def get_response(click_type, clicker_id, clicker_email, original_message, request_record):
    if click_type == 'mentee_claimed':
        mentor_id = Airtable.mentor_id_from_slack_email(clicker_email)
        if mentor_id:
            attachment = mentee_claimed(clicker_id, request_record)
        else:
            attachment = original_message['attachments'][0]
            attachment['text'] = f":warning: <@{clicker_id}>'s Slack Email not found in Mentor table. :warning:"
    else:
        mentor_id = ''
        attachment = mentee_unclaimed(clicker_id, request_record)

    return attachment, mentor_id


def handle_claimed(clicker_id, mentor_id, request_record, original_message):
    if mentor_id:
        attachment = mentee_claimed(clicker_id, request_record)
    else:
        attachment = original_message['attachments'][0]
        attachment['text'] = f":warning: <@{clicker_id}>'s Slack Email not found in Mentor table. :warning:"

    Slack.update_message(**attachment)
