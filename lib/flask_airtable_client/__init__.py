import logging
from functools import lru_cache

import requests

MENTORS_TABLE_NAME = "Mentors"
REQUEST_TABLE_NAME = "Mentor Request"
logger = logging.getLogger('airtable_client')


class AirtableClient:
    def __init__(self, app=None, base=None, api_key=None):
        self.base = base
        self.api_key = api_key
        self.services_id_to_service = {}

        if app is not None and base is not None and api_key is not None:
            self.init_app(app, base, api_key)

    def init_app(self, app, base, api_key):
        self.base = base
        self.api_key = api_key

        app.extensions['airtable_client'] = self

    def get(self, url, **kwargs):
        auth_header = {f'authorization': f"Bearer {self.api_key}"}
        logger.debug(f'Sending airtable request to url {url} and kwargs {kwargs}')
        response = requests.get(url, headers=auth_header, **kwargs)
        logger.info(f'Response from airtable request to {url}: {response}')
        return response

    def patch(self, url, **kwargs):
        auth_header = {f'authorization': f"Bearer {self.api_key}"}
        logger.debug(f'Sending airtable patch to url {url} and kwargs {kwargs}')
        response = requests.patch(url, headers=auth_header, **kwargs)
        logger.info(f'Response from airtable request to {url}: {response}')
        return response

    def table_url(self, table_name, record_id=None):
        url = f'https://api.airtable.com/v0/{self.base}/{table_name}'
        if record_id:
            url += f'/{record_id}'
        return url

    def translate_service_id(self, service_id):
        if self.services_id_to_service:
            return self.services_id_to_service[service_id]

        url = self.table_url("Services")
        params = {'fields[]': 'Name'}
        res = self.get(url, params=params)
        records = res.json()['records']
        self.services_id_to_service = {record['id']: record['fields']['Name'] for record in records}
        return self.services_id_to_service[service_id]

    @lru_cache(64)
    def get_mentor_from_record_id(self, record_id: str) -> dict:
        url = self.table_url("Mentors", record_id)
        res = self.get(url)
        if res.ok:
            return res.json()['fields']
        else:
            return {}

    def find_mentors_with_matching_skillsets(self, skillsets):
        url = self.table_url("Mentors")
        params = {'fields': ['Email', 'Skillsets', 'Slack Name']}
        skillsets = skillsets.split(',')
        mentors = self.get(url, params=params).json()['records']
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

    def mentor_id_from_slack_email(self, email):
        url = self.table_url("Mentors")
        params = {"filterByFormula": f"FIND(LOWER('{email}'), LOWER({{Email}}))"}

        response = self.get(url, params=params)
        if response.ok:
            records = response.json()['records']
            if records:
                return records[0]['id']
            else:
                return ''
        else:
            return ''

    def update_request(self, request_record, mentor_id):
        url = self.table_url("Mentor Request", request_record)
        data = {
            "fields": {
                "Mentor Assigned": [mentor_id] if mentor_id else None
            }}
        return self.patch(url, json=data)
