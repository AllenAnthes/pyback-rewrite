from pyback import slack_client
from pyback.slack.utils.topic_suggestion_messages import new_suggestion_community_message


def help_topic_suggestion(user: dict, submission: dict, **rest: dict) -> None:
    user_id = user['id']
    suggestion = submission['suggestion']

    slack_client.user_name_from_id(user_id)
    slack_message = new_suggestion_community_message(user_id, suggestion)
    community = slack_client.channels['community']
    slack_client.post_message(channel=community, message=slack_message)
