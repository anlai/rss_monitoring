# Load pkgs
from twilio.rest import Client
import feedparser
import time
import pytz
from datetime import date, datetime
import smtplib, ssl

import settings

# Setup Twilio Client for sending messages
client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)

# Set Timezone to UTC/GMT
# UTC = pytz.utc
tz = pytz.timezone(settings.TZ)

# Function to send notification (Current: Message by Twilio)
def sendNoti(feed):
    msg = "New changes detected:" + "\n--------\n"
    for entry in feed.entries:
        # Get current time
        currentTime = datetime.now(UTC)

        # Matching day/hour
        if (entry['published_parsed'].tm_mday == currentTime.day) and abs(((entry['published_parsed'].tm_hour - currentTime.hour)) <= 1) and abs(((entry['published_parsed'].tm_min - currentTime.minute)) <= 5):
            title = entry['title']
            link = entry['link']
            published = entry['published']
            
            # Build the message to send later
            msg = msg + title + "\n" + link + "\n" + published + "\n------------\n"

    # Send the built message
    match settings.NOTIFICATION:
        case 'twilio':
            sendTwilio(msg)
        case 'email':
            sendEmail(msg)

    debugOutput(f'Sent msg: {msg}')

def sendTwilio(msg):
    message = client.messages \
                .create(
                     body=msg,
                     from_=settings.TWILIO_FROM,
                     to=settings.TWILIO_TO
                 )

def sendEmail(msg):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL_SERVER, settings.EMAIL_PORT, context=context) as server:
        server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
        server.sendmail(settings.EMAIL_USER, settings.EMAIL_TO, msg)

# calls to load data from the feed, including retry logic
def loadFeed():

    debugOutput("Attempting to load feed data")

    feed = feedparser.parse(settings.RSS_URL)

    debugOutput(f"Received {feed.status} from call")

    while feed.status != 200:
        if feed.status == 429:
            retryAfter = int(feed.headers['retry-after'])
            debugOutput(f"Waiting for {retryAfter} seconds for retry...")
            time.sleep(retryAfter+1) # wait an additional second
        else:
            debugOutput(f"Recieved status {feed.status}, waiting normal interval for retry...")
            time.sleep(settings.INTERVAL)
        
        feed = feedparser.parse(settings.RSS_URL)

    return feed

def debugOutput(msg):
    if settings.VERBOSE:
        print(f"DEBUG: {msg}")

# Driver Function
def main():

    print("Initializing...")

    # Get the data
    feed = loadFeed()

    # Get latest changes made
    default = None
    if len(feed.entries) > 0:
        default = feed.entries[0].published
    else:
        debugOutput('No entries in the feed...')

    print("Start!")
    print(f"Target URL: {settings.RSS_URL}")
    print("." + "\n" + "." + "\n" + "." + "\n")

    while True:
        try:
            print(f"Waiting for {settings.INTERVAL} seconds...")
            time.sleep(settings.INTERVAL)
            # Update current time
            currentTime = datetime.now(tz)
            currentTime = currentTime.strftime("%I:%M %p")

            # Get new data
            feed = loadFeed()

            # Get the lastest published time again to check for any changes
            # Only if results come back, otherwise it doesn't change
            check = None
            if len(feed.entries) > 0:
                check = feed.entries[0].published
            else:
                debugOutput('No entries in the feed...')

            # Different published time means the RSS was updated with new data.
            if check != default:
                # Send notification to number in TWILIO 
                sendNoti(feed)
                print(f"--->Changes detected! Message sent at {currentTime}<---")
                print("--------------------------\n")
                debugOutput(f'Default (before changed): {default}')
                debugOutput(f'Check: {check}')

                # Update default with new changes
                default = check
                
            else:
                print(f'No detected changes at {currentTime}')
                print("--------------------------")

        except Exception as e:
            print("---------- WARNING ----------")
            print("Error occured! Check below:")
            print("Exception: {}".format(type(e).__name__))
            print("Exception message: {}".format(e))
            print("-----------------------------")
            
if __name__ == "__main__":
    main()