from typing import List

from pyback.utils import now


def make_greeting_messages(real_name):
    text_greet = {
        'text': f"Hi {real_name},\n\n"
                "Welcome to Operation Code! I'm a bot designed to help answer questions and "
                "get you on your way in our community.\n\n "
                "Our goal here at Operation Code is to get veterans and their families started on the path to a career "
                "in programming. We do that through providing you with scholarships, mentoring, career development "
                "opportunities, conference tickets, and more!\n"
    }

    external_buttons = {
        "text": "Much of the provided aid requires veteran or military spouse status. Please verify your status on "
                "your profile at https://operationcode.org/ if you haven't already.\n\n"
                "You're currently in Slack, a chat application that serves as the hub of Operation Code. "
                "If you're visiting us via your browser, Slack provides a stand alone program to make staying in "
                "touch even more convenient.\n\n"
                "All active Operation Code projects are located on our source control repository. "
                "Our projects can be viewed on GitHub\n\n"
                "Lastly, please take a moment to review our Code of Conduct.",
        "attachments": [{
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "external_buttons",
            "attachment_type": "default",
            "actions": [{
                "name": "github",
                "text": "GitHub",
                "type": "button",
                "value": "github",
                "url": "https://github.com/OperationCode"
            }, {
                "name": "download",
                "text": "Slack Client",
                "type": "button",
                "value": "download",
                "url": "https://slack.com/downloads"
            }, {
                "name": "code_of_conduct",
                "text": "Code of Conduct",
                "type": "button",
                "value": "code_of_conduct",
                "url": "https://github.com/OperationCode/community/blob/master/code_of_conduct.md"
            }]
        }]
    }

    base_resources = {
        "text": "We recommend the following resources.",
        "attachments": [{
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "resource_buttons",
            "attachment_type": "default",
            "actions": [{
                "name": "javascript",
                "text": "JavaScript",
                "type": "button",
                "value": "javascript"
            }, {
                "name": "python",
                "text": "Python",
                "type": "button",
                "value": "python"
            }, {
                "name": "ruby",
                "text": "Ruby",
                "type": "button",
                "value": "ruby"
            }]
        }, {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "suggestion",
            "attachment_type": "default",
            "actions": [{
                "name": "suggestion_button",
                "text": "Are we missing something? Click!",
                "type": "button",
                "value": "suggestion_button"
            }]
        }]
    }

    return [text_greet, external_buttons, base_resources]


def new_member_community_announcement(user_id):
    return {
        'text': f':tada: <@{user_id}> has joined! :tada:',
        'attachments': not_greeted_response()
    }


def greet_button_template(original_message, channel, message_ts) -> dict:
    return {
        'text': original_message['text'],
        'channel': channel['id'],
        'ts': message_ts,
        # 'as_user': True
    }


def greeted_response(user_id) -> List[dict]:
    return [{
        "text": f":100:<@{user_id}> has greeted the new user!:100:\n"
                f"<!date^{now()}^Greeted at {{date_num}} {{time_secs}}|Failed to parse time>",
        "fallback": "",
        "color": "#3AA3E3",
        "callback_id": "greeted",
        "attachment_type": "default",
        "actions": [{
            "name": "reset_greet",
            "text": f"Reset claim",
            "type": "button",
            "style": "danger",
            "value": "reset_greet",
        }]
    }]


def not_greeted_response():
    return [{
        'text': "",
        "fallback": "Someone should greet them!",
        "color": "#3AA3E3",
        "callback_id": "greeted",
        "attachment_type": "default",
        "actions": [{
            "name": "greeted",
            "text": "I will greet them!",
            "type": "button",
            "style": "primary",
            "value": "greeted"
        }]
    }]


def reset_greet_message(user_id):
    return (f"Reset by <@{user_id}> at"
            f" <!date^{now()}^ {{date_num}} {{time_secs}}|Failed to parse time>")
