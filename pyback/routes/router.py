from pyback.handlers import default_handler
from pyback.handlers.airtable_handlers import mentor_request
from ..handlers.slack_handlers import new_member, member_greeted, action_menu, suggestion, claim_mentee


def route_request(event: dict):
    event_type = event['type']
    handler = get_handler(event_type)
    handler(**event)


def get_handler(event_type: str):
    return event_handlers.get(event_type, default_handler)


def interactive_message_handler(**event):
    interaction = event['callback_id']
    handler = interaction_handlers.get(interaction, default_handler)
    handler(**event)


event_handlers = {
    'team_join': new_member,
    'interactive_message': interactive_message_handler,
    'mentor_request': mentor_request
}

interaction_handlers = {
    'greeted': member_greeted,
    'resource_buttons':  action_menu,
    'suggestion': suggestion,
    'claim_mentee': claim_mentee,
}
