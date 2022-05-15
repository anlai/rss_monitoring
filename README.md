# A Python script to monitor RSS and send notifications to registerd user.

Script runs in an infinite loop and monitors an RSS feed for changes.  Once a change is detected, it sends a notification via the selected method (Twilio or email).

There are two methods to run the script, either locally or via Docker container.  At this time it has only been tested against rpilocator.com, it can be configured to monitor other feeds, but YMMV.

## Local

If you wish to execute the script locally you have a couple of options to store the secrets (global environment variables, virtual envirnment variables or using a .env file).  Once you have that setup, you can start the script using `python3 rpilocator.py` and it'll run in an infinite loop.

## Docker

**docker cli**

Twilio using all default settings for rpilocator

```
docker run -d \
    --name=rss-monitor \
    -e TWILIO_SID= \
    -e TWILIO_TOKEN= \
    -e TWILIO_TO= \
    -e TWILIO_FROM= \
    ghcr.io/anlai/rss_monitoring:latest
```

Email using all default settings for rpilocator

```
docker run -d \
    --name=rss-monitoring \
    -e NOTIFICATION=email \
    -e EMAIL_SERVER=smtp.gmail.com \
    -e EMAIL_USER={email username} \
    -e EMAIL_PASS={email password} \
    -e EMAIL_TO={recipient} \
    ghcr.io/anlai/rss_monitoring:latest
```

## Configuration

Configuration of the script is done via environment variables, if not set the values will default to the default value specified in the table.

| Name | Required | Default Value | Purpose |
| --- | --- | --- | --- |
| RSS_URL | false | https://rpilocator.com/feed/?country=US | RSS URL to monitor |
| INTERVAL | false | 30 | Seconds to wait between checks of the feed |
| NOTIFICATION | false | Twilio | Which method to use to notify you of a change (options: twilio, email) |
| EMAIL_SERVER | false* | NOT_SET | Email server url (eg. smtp.gmail.com) | 
| EMAIL_PORT | false* | 465 | This is the default port for gmail over ssl |
| EMAIL_USER | false* | NOT_SET | Username to authenticate to SMTP server |
| EMAIL_PASS | false* | NOT_SET | Password to authenticate to SMTP server |
| EMAIL_TO | false* | NOT_SET | Email recipient |
| TWILIO_SID | false* | NOT_SET | Twilio account SID |
| TWILIO_TOKEN | false* | NOT_SET | Twilio account token |
| TWILIO_TO | false* | NOT_SET | Twilio recipient |
| TWILIO_FROM | false* | NOT_SET | Twilio phone number to send from |
| VERBOSE | false | False | Enable debug output in the logs |

\* Depending on NOTIFICATION you need to provide the associated config settings for either EMAIL_* or TWILIO_* to work.

## Credit

I forked the script from https://github.com/huynggg/rss_monitoring and enhanced it to suit my needs (docker-ized and support email).