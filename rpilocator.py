# Load pkgs
from config.secrets import *
from twilio.rest import Client
import feedparser
import hashlib
import json
import time
import pytz
from datetime import date, datetime

# Setup Twilio Client for sending messages
client = Client(TWILIO_SID, TWILIO_TOKEN)

# Get current time at GMT/UTC
UTC = pytz.utc
currentTime = datetime.now(UTC)

# Config object

config = {
    "URL": "https://rpilocator.com/feed/",
    "waitTime": 15,
}

# Target URL.

# Function to send notification (Current: Message by Twilio)
def sendNoti(feed):
    msg = "New changes detected:" + "\n--------"
    for entry in feed.entries:
        # Matching day/hour
        if (entry['published_parsed'].tm_mday == currentTime.day) and ((entry['published_parsed'].tm_hour - currentTime.hour) <= 1) and ((entry['published_parsed'].tm_min - currentTime.minute) <= 10):
            title = entry['title']
            link = entry['link']
            published = entry['published']
            
            # Build the message to send later
            msg = msg + title + "\n" + link + "\n" + published + "\n------------"

    # Send the built message
    message = client.messages \
                .create(
                     body=msg,
                     from_=TWILIO_FROM,
                     to=TWILIO_TO
                 )
# Driver Function
def main():
    # Get the data
    feed = feedparser.parse(config["URL"])

    # Get latest changes made
    default = feed.entries[0].published

    # Default hashed value
    # default = get_hash(feed.entries).hex()
    
    print("Start!")
    print(f"Target URL: {config['URL']}")
    print("." + "\n" + "." + "\n" + "." + "\n")

    while True:
        try:
            print(f"Monitoring the RSS...")
            time.sleep(config["waitTime"])
            # Update current time
            currentTime = datetime.now(UTC)
            currentTime = currentTime.strftime("%H:%M:%S")

            # Get new data
            feed = feedparser.parse(config['URL'])

            # Get the lastest published time again to check for any changes
            check = feed.entries[0].published

            # Different published time means the RSS was updated with new data.
            if check != default:
                # Send notification
                sendNoti(feed)
                print(f"--->Changes detected! Message sent at {currentTime}<---")
                print("--------------------------")

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
