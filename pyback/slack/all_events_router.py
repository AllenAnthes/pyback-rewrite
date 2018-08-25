from pyback.slack.event_handlers import new_member, member_greeted, action_menu, \
    open_suggestion, claim_mentee, default_handler, mentor_request
from pyback.slack.dialog_handlers import help_topic_suggestion

"""
This module routes slack events to the correct handler function

If the event is a standard event (e.g. 'team join' when someone joins slack for the first time)
the handler is simply returned and called

If the event is a more specific event, for example an interactive message, another function is called
to route to the correct interactive message handler
"""


def route_request(event: dict):
    event_type = event['type']
    handler = event_handlers.get(event_type, default_handler)
    handler(**event)


def interactive_message_handler(**event):
    interaction = event['callback_id']
    handler = interaction_handlers.get(interaction, default_handler)
    handler(**event)


def dialog_submission_handler(**event):
    callback_id = event['callback_id']
    handler = dialog_handlers.get(callback_id, default_handler)
    handler(**event)


event_handlers = {
    'team_join': new_member,
    'interactive_message': interactive_message_handler,
    'dialog_submission': dialog_submission_handler,
    'mentor_request': mentor_request
}

interaction_handlers = {
    'greeted': member_greeted,
    'resource_buttons': action_menu,
    'suggestion': open_suggestion,
    'claim_mentee': claim_mentee,
}

dialog_handlers = {
    'suggestion_modal': help_topic_suggestion
}
