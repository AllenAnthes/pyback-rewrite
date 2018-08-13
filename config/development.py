from decouple import config

PORT = 5000

TOKEN = config('DEV_BOT_TOKEN', default='token')
VERIFICATION_TOKEN = config('DEV_AUTH_TOKEN', default='token')
COMMUNITY_CHANNEL = config('DEV_COMMUNITY_CHANNEL', default='community_channel')
MENTORS_INTERNAL_CHANNEL = config('DEV_MENTORS_CHANNEL', default='mentor_channel')

AIRTABLE_BASE_KEY = config('DEV_AIRTABLE_BASE_KEY', default='fake_airtable_base')
AIRTABLE_API_KEY = config('DEV_AIRTABLE_TOKEN', default='fake_airtable_key')

SQLALCHEMY_DATABASE_URI = config('DEV_DATABASE_URI')

RECAPTCHA_SECRET = config('RECAPTCHA_SECRET')
GITHUB_JWT = config('GITHUB_JWT')
GITHUB_REPO_PATH = config('DEV_GITHUB_REPO_PATH')

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')