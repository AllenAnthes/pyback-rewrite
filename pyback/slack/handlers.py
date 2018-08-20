from pyback.slack.utils.mentor_request_messages import new_request_announcement, request_details, matching_mentors
from pyback.slack.utils.mentor_request_messages import mentee_claimed, mentee_unclaimed, base_claim_message
from pyback.slack.utils.action_menu_messages import suggestion_modal, action_menu_message
from pyback import airtable_client as Airtable
from pyback import slack_client as slack
from pyback.slack.utils.greeting_messages import *


def new_member(user, **other):
    user_id = user['id']
    real_name = slack.user_name_from_id(user_id)

    user_messages = make_greeting_messages(real_name)
    community_message = new_member_community_announcement(real_name)

    for message in user_messages:
        slack.post_message(channel=user_id, message=message)

    channel = slack.channels['community']
    slack.post_message(channel=channel, message=community_message)


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

    slack.update_message(**updated_button)


def action_menu(actions, channel, message_ts, **other):
    """
    Handles the interactive message sent to a new user when
    they first join
    """
    action_button = actions[0]['name']
    updated_message = action_menu_message(action_button, channel, message_ts)
    slack.update_message(**updated_message)


def suggestion(trigger_id, **rest):
    """
    Tells slack to open the suggestion modal when the user clicks the suggestion button
    """
    dialog = suggestion_modal(trigger_id)
    slack.open_dialog(**dialog)


def claim_mentee(user, actions, original_message, channel, message_ts, **rest):
    clicker_id = user['id']
    click_type = actions[0]['value']
    request_record = actions[0]['name']
    user_info = slack.user_info_from_id(clicker_id)
    clicker_email = user_info['user']['profile']['email']
    message = base_claim_message(original_message, channel['id'], message_ts)

    attachment, mentor_id = get_response(click_type, clicker_id, clicker_email, original_message, request_record)

    message['attachments'] = attachment
    slack.update_message(**message)

    Airtable.update_request(request_record, mentor_id)


def get_response(click_type, clicker_id, clicker_email, original_message, request_record):
    if click_type == 'mentee_claimed':
        mentor_id = Airtable.mentor_id_from_slack_email(clicker_email)
        if mentor_id:
            attachment = mentee_claimed(clicker_id, request_record)
        else:
            attachment = original_message['attachments'][0]
            attachment['text'] = f":warning: <@{clicker_id}>'s slack Email not found in Mentor table. :warning:"
    else:
        mentor_id = ''
        attachment = mentee_unclaimed(clicker_id, request_record)

    return attachment, mentor_id


def handle_claimed(clicker_id, mentor_id, request_record, original_message):
    if mentor_id:
        attachment = mentee_claimed(clicker_id, request_record)
    else:
        attachment = original_message['attachments'][0]
        attachment['text'] = f":warning: <@{clicker_id}>'s slack Email not found in Mentor table. :warning:"

    slack.update_message(as_user=True, **attachment)


def mentor_request(email, slack_user, record, service, requested_mentor: str = None, skillsets: str = None,
                   details='None Given', **other):
    slack_id = slack.user_id_from_email(email, fallback=slack_user)
    service_translation = Airtable.translate_service_id(service)
    requested_mentor_message = get_requested_mentor(requested_mentor)
    mentors = get_matching_skillset_mentors(skillsets)

    first_message = new_request_announcement(slack_id, service_translation, record, skillsets, requested_mentor_message)
    details_message = request_details(details)
    matching_mentors_message = matching_mentors(mentors)

    post_messages(first_message, [details_message, matching_mentors_message])


def post_messages(parent, children):
    channel = slack.channels['mentors']
    response = slack.post_message(channel, parent)
    timestamp = response['ts']

    for child in children:
        child['thread_ts'] = timestamp
        slack.post_message(channel, child)


def get_matching_skillset_mentors(skillsets):
    if not skillsets:
        return ['No skillset Given']
    mentors = Airtable.find_mentors_with_matching_skillsets(skillsets)
    return [slack.user_id_from_email(mentor['Email'], fallback=mentor['slack Name']) for mentor in mentors]


def get_requested_mentor(requested_mentor):
    try:
        if not requested_mentor:
            return None
        mentor = Airtable.get_mentor_from_record_id(requested_mentor)
        email = mentor['Email']
        slack_user_id = slack.user_id_from_email(email)
        return f" Requested mentor: {slack_user_id}"
    except Exception as ex:
        return None


def default_handler(**event):
    pass
