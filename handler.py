import json
import numpy as np
import requests
import time
from bs4 import BeautifulSoup
from twilio.rest import Client


def numpy_test(event, context):
    a = np.arange(15).reshape(3, 5)

    print "Your numpy array:"
    print a

# some hard-coded credential, not a good practice in prod or github repo
sid = 'TODO'
token = 'TODO'
from_num = 'TODO'
to = 'TODO'


def scrape_availability(url):
    search_query = "TODO_SEARCHQUERY"
    return requests.post(url=url, data=search_query)


def send_sms(msg):
    twilio_cli = Client(sid, token)
    twilio_cli.messages.create(body=msg, from_=from_num, to=to)


def search_by_codes(html_obj, old_houses_code=('rmlist8', 'rmlist9', 'rmlist10')):
    for code in old_houses_code:
        house = html_obj.body.find('div', attrs={'id': code})
        house_name = house.find('div', "panel-title text-dark").text.strip()
        if house.text.find('Reserve') > -1:
            msg = 'House {} is available for booking'.format(house_name)
            print msg
            send_sms(msg)
        # else:
        #     print 'House {} is NOT available for booking'.format(house_name)


def scrape_ys_old_houses(event, context):
    try:
        try_count = 0
        while True:
            try_count += 1
            print 'Attempt # {}'.format(try_count)
            # url webevent ID can expire
            url = 'TODO-WEBURL'
            r = scrape_availability(url)
            if r.status_code == 200:
                search_by_codes(BeautifulSoup(r.content))
            interval = 60
            time.sleep(interval)
    except requests.exceptions.ConnectionError:
        send_sms('URL web event ID probably needs a refresh')


if __name__ == "__main__":
    numpy_test('', '')