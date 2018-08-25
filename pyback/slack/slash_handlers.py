from flask import make_response
from slack import methods

from pyback import slack_client
from pyback.database.models import Channel, User


def slash_here(channel, text, slack_id):
    if not can_here(channel, slack_id):
        return make_response("You are not authorized to use that command in this channel")
    channel_members_response = slack_client.api_call(methods.CONVERSATIONS_MEMBERS, channel=channel)
    member_list = [f'<@{member}>' for member in channel_members_response['members']]
    members = ' '.join(member_list)
    message = {'text': members + text}
    post_message_response = slack_client.post_message(channel, message)
    return make_response('', 200)


def can_here(channel_id, user_id):
    user = User.query.filter_by(slack_id=user_id).first()
    channel = Channel.query.filter_by(channel_id=channel_id).first()
    return channel is not None and user in channel.mods
