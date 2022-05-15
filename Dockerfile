FROM python:3

ADD . /rss

WORKDIR /rss
RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "/rss/rpilocator.py"]