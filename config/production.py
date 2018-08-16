from decouple import config

SECRET_KEY = config('SECRET_KEY')

TOKEN = config('OPCODE_TOKEN')
VERIFICATION_TOKEN = config('OPCODE_VERIFICATION_TOKEN')
COMMUNITY_CHANNEL = config('OPCODE_COMMUNITY_ID')
MENTORS_INTERNAL_CHANNEL = config('OPCODE_MENTORS_INTERNAL_CHANNEL')

AIRTABLE_BASE_KEY = config('OPCODE_AIRTABLE_BASE_KEY')
AIRTABLE_API_KEY = config('OPCODE_AIRTABLE_TOKEN')

SQLALCHEMY_DATABASE_URI = config('PROD_DATABASE_URI')

RECAPTCHA_SECRET = config('RECAPTCHA_SECRET')
GITHUB_JWT = config('GITHUB_JWT')
GITHUB_REPO_PATH = config('GITHUB_REPO_PATH')

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')