from pyback import app
from pyback.external.airtable_client import Airtable
from pyback.external.slack_client import Slack
from pyback.utils.mentor_request_messages import new_request_announcement, request_details, matching_mentors

channel = app.config['MENTORS_INTERNAL_CHANNEL']


def mentor_request(email, slack_user, record, service, requested_mentor: str = None, skillsets: str = None,
                   details='None Given', **other):
    slack_id = Slack.user_id_from_email(email, fallback=slack_user)
    service_translation = Airtable.translate_service_id(service)
    requested_mentor_message = get_requested_mentor(requested_mentor)
    mentors = get_matching_skillset_mentors(skillsets)

    first_message = new_request_announcement(slack_id, service_translation, record, skillsets, requested_mentor_message)
    details_message = request_details(details)
    matching_mentors_message = matching_mentors(mentors)

    post_messages(first_message, [details_message, matching_mentors_message])


def post_messages(parent, children):
    response = Slack.post_message(channel, parent)
    timestamp = response['ts']

    for child in children:
        child['thread_ts'] = timestamp
        Slack.post_message(channel, child)


def get_matching_skillset_mentors(skillsets):
    if not skillsets:
        return ['No skillset Given']
    mentors = Airtable.find_mentors_with_matching_skillsets(skillsets)
    return [Slack.user_id_from_email(mentor['Email'], fallback=mentor['Slack Name']) for mentor in mentors]


def get_requested_mentor(requested_mentor):
    try:
        if not requested_mentor:
            return None
        mentor = Airtable.get_mentor_from_record_id(requested_mentor)
        email = mentor['Email']
        slack_user_id = Slack.user_id_from_email(email)
        return f" Requested mentor: {slack_user_id}"
    except Exception as ex:
        return None
