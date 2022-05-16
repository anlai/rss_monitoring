import os

# interval between checks (in seconds)
RSS_URL = os.environ.get('RSS_URL') or 'https://rpilocator.com/feed/?country=US'
INTERVAL = 30

# what type of notification to use 
# options: twilio, email
NOTIFICATION = os.environ.get('NOTIFICATION') or 'twilio'

# email settings
EMAIL_SERVER = os.environ.get('EMAIL_SERVER') or 'NOT_SET'
EMAIL_PORT = os.environ.get('EMAIL_PORT') or 465
EMAIL_USER = os.environ.get('EMAIL_USER') or 'NOT_SET'
EMAIL_PASS = os.environ.get('EMAIL_PASS') or 'NOT_SET'
EMAIL_TO = os.environ.get('EMAIL_TO') or 'NOT_SET'

# twilio settings
TWILIO_SID = os.environ.get('TWILIO_SID') or 'NOT_SET'
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN') or 'NOT_SET'
TWILIO_TO = os.environ.get('TWILIO_TO') or 'NOT_SET' # twilio phone number
TWILIO_FROM = os.environ.get('TWILIO_FROM') or 'NOT_SET' # sms recipient

TZ = os.environ.get('TZ') or 'UTC'

# debug settings
VERBOSE = os.environ.get('VERBOSE') or False