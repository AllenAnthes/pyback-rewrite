from typing import List

from pyback.utils import now


def new_request_announcement(user_id, service, record, skillsets='None provided', requested_mentor_message=None):
    message = {
        'text': f"User {user_id} has requested a mentor for {service}\n\n"
                f"Requested Skillset(s): {skillsets.replace(',', ', ')}",
        'attachments': claim_mentee_button(record)
    }

    if requested_mentor_message:
        message['text'] += requested_mentor_message

    return message


def claim_mentee_button(record: str) -> List[dict]:
    return [{
        'text': '',
        'fallback': '',
        'color': '#3AA3E3',
        'callback_id': 'claim_mentee',
        'attachment_type': 'default',
        'actions': [{
            'name': f'{record}',
            'text': 'Claim Mentee',
            'type': 'button',
            'style': 'primary',
            'value': f'mentee_claimed',
        }]
    }]


def request_details(details: str):
    if not details:
        return {
            'text': 'None Given',
        }
    return {
        'text': f"Additional details: {details}",
    }


def base_claim_message(original_message, channel_id, message_ts):
    return {
        'text': original_message['text'],
        'channel': channel_id,
        'ts': message_ts,
        'as_user': True
    }


def mentee_claimed(user_id: str, record: str) -> List[dict]:
    return [{
        "text": f":100: Request claimed by <@{user_id}>:100:\n"
                f"<!date^{now()}^Claimed at {{date_num}} {{time_secs}}|Failed to parse time>",
        "fallback": "",
        "color": "#3AA3E3",
        "callback_id": "claim_mentee",
        "attachment_type": "default",
        "actions": [{
            'name': f'{record}',
            "text": f"Reset claim",
            "type": "button",
            "style": "danger",
            "value": "reset_claim_mentee",
        }]
    }]


def mentee_unclaimed(user_id: str, record: str) -> List[dict]:
    return [{
        'text': f"Reset by <@{user_id}> at"
                f" <!date^{now()}^ {{date_num}} {{time_secs}}|Failed to parse time>",
        'fallback': '',
        'color': '#3AA3E3',
        'callback_id': 'claim_mentee',
        'attachment_type': 'default',
        'actions': [{
            'name': f'{record}',
            'text': 'Claim Mentee',
            'type': 'button',
            'style': 'primary',
            'value': 'mentee_claimed'
        }]
    }]


def matching_mentors(mentors: list):
    return {
        'text': "Mentors matching all or some of the requested skillsets: " + ' '.join(mentors),
    }
