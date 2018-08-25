from typing import Dict, Any, Optional

from pyback.slack.utils.mentor_request_messages import new_request_announcement, request_details, matching_mentors
from pyback.slack.utils.mentor_request_messages import mentee_claimed_message, mentee_unclaimed, base_claim_message
from pyback.slack.utils.action_menu_messages import suggestion_modal_message, action_menu_message
from pyback import airtable_client as Airtable
from pyback import slack_client
from pyback.slack.utils.greeting_messages import *


def new_member(user: Dict[str, Any], **other) -> None:
    user_id = user['id']
    real_name = slack_client.user_name_from_id(user_id)

    user_messages = make_greeting_messages(real_name)
    community_message = new_member_community_announcement(real_name)

    for message in user_messages:
        slack_client.post_message(channel=user_id, message=message)

    channel = slack_client.channels['community']
    slack_client.post_message(channel=channel, message=community_message)


def member_greeted(user: Dict[str, Any], actions: list, original_message: Dict[str, Any], channel: Dict[str, str],
                   message_ts: str, **other) -> None:
    user_id = user['id']
    updated_button = greet_button_template(original_message, channel, message_ts)
    click_type = actions[0]['value']

    if click_type == 'greeted':
        updated_button['attachments'] = greeted_response(user_id)
    else:
        updated_button['attachments'] = not_greeted_response()

        if click_type == 'reset_greet':
            updated_button['attachments'][0]['text'] = reset_greet_message(user_id)

    slack_client.update_message(**updated_button)


def action_menu(actions: list, channel: Dict[str, str], message_ts: str, **other) -> None:
    """
    Handles the interactive message sent to a new user when
    they first join
    """
    action_button = actions[0]['name']
    updated_message = action_menu_message(action_button, channel, message_ts)
    slack_client.update_message(**updated_message)


def open_suggestion(trigger_id: str, **rest) -> None:
    """
    Tells slack to open the suggestion modal when the user clicks the suggestion button
    """
    dialog = suggestion_modal_message(trigger_id)
    slack_client.open_dialog(**dialog)


# def handle_claimed(clicker_id: str, mentor_id: str, request_record: str, original_message: dict):
#     if mentor_id:
#         attachment = mentee_claimed_message(clicker_id, request_record)
#     else:
#         attachment = original_message['attachments'][0]
#         attachment['text'] = f":warning: <@{clicker_id}>'s slack Email not found in Mentor table. :warning:"
#
#     slack.update_message(**attachment)


def claim_mentee(user: dict, actions: list, original_message: dict, channel: dict, message_ts: str,
                 **rest: dict) -> None:
    clicker_id = user['id']
    click_type = actions[0]['value']
    request_record = actions[0]['name']
    user_info = slack_client.user_info_from_id(clicker_id)
    clicker_email = user_info['user']['profile']['email']
    message = base_claim_message(original_message, channel['id'], message_ts)

    attachment, mentor_id = _create_claim_mentee_response(click_type, clicker_id, clicker_email, original_message,
                                                          request_record)

    message['attachments'] = attachment
    slack_client.update_message(**message)

    Airtable.update_request(request_record, mentor_id)


def mentor_request(email: str, slack_user: str, record: str, service: str, requested_mentor: str = None,
                   skillsets: str = None, details: str = 'None Given', **other) -> None:
    slack_id = slack_client.user_id_from_email(email, fallback=slack_user)
    service_translation = Airtable.translate_service_id(service)
    requested_mentor_message = _get_requested_mentor(requested_mentor)
    mentors = _get_matching_skillset_mentors(skillsets)

    first_message = new_request_announcement(slack_id, service_translation, record, skillsets, requested_mentor_message)
    details_message = request_details(details)
    matching_mentors_message = matching_mentors(mentors)

    _post_messages(first_message, [details_message, matching_mentors_message])


def _create_claim_mentee_response(click_type: str, clicker_id: str, clicker_email: str, original_message: dict,
                                  request_record: str) -> tuple:
    if click_type == 'mentee_claimed':
        mentor_id = Airtable.mentor_id_from_slack_email(clicker_email)
        if mentor_id:
            attachment = mentee_claimed_message(clicker_id, request_record)
        else:
            attachment = original_message['attachments'][0]
            attachment['text'] = f":warning: <@{clicker_id}>'s slack Email not found in Mentor table. :warning:"
    else:
        mentor_id = ''
        attachment = mentee_unclaimed(clicker_id, request_record)

    return attachment, mentor_id


def _post_messages(parent: Dict[str, Any], children: List[dict]) -> None:
    channel = slack_client.channels['mentors']
    response = slack_client.post_message(channel, parent)
    timestamp = response['ts']

    for child in children:
        child['thread_ts'] = timestamp
        slack_client.post_message(channel, child)


def _get_matching_skillset_mentors(skillsets: str) -> List[str]:
    if not skillsets:
        return ['No skillset Given']
    mentors = Airtable.find_mentors_with_matching_skillsets(skillsets)
    return [slack_client.user_id_from_email(mentor['Email'], fallback=mentor['Slack Name']) for mentor in mentors]


def _get_requested_mentor(requested_mentor: Optional[str]) -> Optional[str]:
    try:
        if not requested_mentor:
            return None
        mentor = Airtable.get_mentor_from_record_id(requested_mentor)
        email = mentor['Email']
        slack_user_id = slack_client.user_id_from_email(email)
        return f" Requested mentor: {slack_user_id}"
    except Exception as ex:
        return None


def default_handler(**event) -> None:
    pass
