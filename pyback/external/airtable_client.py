from functools import lru_cache

from requests import get, patch
from pyback import app

logger = app.logger
configs = app.config

BASE = configs['AIRTABLE_BASE_KEY']
API_KEY = configs['AIRTABLE_API_KEY']
MENTORS_TABLE_NAME = "Mentors"
REQUEST_TABLE_NAME = "Mentor Request"
auth_header = {f'authorization': f"Bearer {API_KEY}"}


def get_configs():
    with app.app_context():
        return app.config


class Airtable:
    services_id_to_service = {}

    @classmethod
    def get(cls, url, **kwargs):
        logger.debug(f'Sending airtable request to url {url} and kwargs {kwargs}')
        response = get(url, headers=auth_header, **kwargs)
        logger.info(f'Response from airtable request to {url}: {response}')
        return response

    @classmethod
    def patch(cls, url, **kwargs):
        logger.debug(f'Sending airtable patch to url {url} and kwargs {kwargs}')
        response = patch(url, headers=auth_header, **kwargs)
        logger.info(f'Response from airtable request to {url}: {response}')
        return response

    @classmethod
    def table_url(cls, table_name, record_id=None):
        url = f'https://api.airtable.com/v0/{BASE}/{table_name}'
        if record_id:
            url += f'/{record_id}'
        return url

    @classmethod
    def translate_service_id(cls, service_id):
        if cls.services_id_to_service:
            return cls.services_id_to_service[service_id]

        url = cls.table_url("Services")
        params = {'fields[]': 'Name'}
        res = cls.get(url, params=params)
        records = res.json()['records']
        cls.services_id_to_service = {record['id']: record['fields']['Name'] for record in records}
        return cls.services_id_to_service[service_id]

    @classmethod
    @lru_cache(64)
    def get_mentor_from_record_id(cls, record_id: str) -> dict:
        url = cls.table_url("Mentors", record_id)
        res = cls.get(url)
        if res.ok:
            return res.json()['fields']
        else:
            return {}

    @classmethod
    def find_mentors_with_matching_skillsets(cls, skillsets):
        # url = cls.table_url("Mentors") + "?fields=Email&fields=Skillsets"
        url = cls.table_url("Mentors")
        params = {'fields': ['Email', 'Skillsets', 'Slack Name']}
        skillsets = skillsets.split(',')
        mentors = cls.get(url, params=params).json()['records']
        partial_match = []
        complete_match = []
        try:
            for mentor in mentors:
                if all(skillset in mentor['fields']['Skillsets'] for skillset in skillsets):
                    complete_match.append(mentor['fields'])
                if any(mentor['fields'] not in complete_match and
                       skillset in mentor['fields']['Skillsets'] for skillset in skillsets):
                    partial_match.append(mentor['fields'])
        except Exception as e:
            logger.warning("Exception occurred while attempting to get matching mentors for skillsets : ", e)

        return complete_match or partial_match

    @classmethod
    def mentor_id_from_slack_email(cls, email):
        url = cls.table_url("Mentors")
        params = {"filterByFormula": f"FIND(LOWER('{email}'), LOWER({{Email}}))"}

        response = cls.get(url, params=params)
        if response.ok:
            records = response.json()['records']
            if records:
                return records[0]['id']
            else:
                return ''
        else:
            return ''

    @classmethod
    def update_request(cls, request_record, mentor_id):
        url = cls.table_url("Mentor Request", request_record)
        data = {
            "fields": {
                "Mentor Assigned": [mentor_id] if mentor_id else None
            }}
        return cls.patch(url, json=data)
