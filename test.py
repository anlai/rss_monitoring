from config.secrets import *
from twilio.rest import Client

client = Client(TWILIO_SID, TWILIO_TOKEN)
msg = "Hello From Myself!"
message = client.messages \
                .create(
                     body=msg,
                     from_=TWILIO_FROM,
                     to=TWILIO_TO
                 )