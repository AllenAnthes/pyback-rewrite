from decouple import config

DEBUG = True

SECRET_KEY = config('DEV_SECRET_KEY', default='secret yo')

TOKEN = config('DEV_BOT_TOKEN', default='token')
APP_TOKEN = config('DEV_APP_TOKEN', default='token')
VERIFICATION_TOKEN = config('DEV_AUTH_TOKEN', default='token')
COMMUNITY_CHANNEL = config('DEV_COMMUNITY_CHANNEL', default='community_channel')
MENTORS_INTERNAL_CHANNEL = config('DEV_MENTORS_CHANNEL', default='mentor_channel')

AIRTABLE_BASE_KEY = config('DEV_AIRTABLE_BASE_KEY', default='fake_airtable_base')
AIRTABLE_API_KEY = config('DEV_AIRTABLE_TOKEN', default='fake_airtable_key')

SQLALCHEMY_DATABASE_URI = config('DEV_DATABASE_URI', default='default')

RECAPTCHA_SECRET = config('RECAPTCHA_SECRET', default='default')
GITHUB_JWT = config('GITHUB_JWT', default='default')
GITHUB_REPO_PATH = config('DEV_GITHUB_REPO_PATH', default='default')

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='default')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='default')
