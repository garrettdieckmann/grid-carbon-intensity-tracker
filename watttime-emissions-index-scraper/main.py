import json
import base64
import urllib3
from os import environ
from google.cloud import pubsub_v1


def scrape_emissions_index(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    replyToTopic = event['attributes']['replyTo'] # TODO: Should handle if no 'replyTo'
    ba_codes = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    if (len(ba_codes) > 0):
        scraper = WattTimeScraper()
        pubsub = PubSub(replyToTopic)
        for ba_code in ba_codes:
            index_data = scraper.get_watttime_index(ba_code)
            pubsub.publish_message(index_data)


class WattTimeScraper:
    def __init__(self):
        self.login_url = 'https://api2.watttime.org/v2/login'
        self.index_url = 'https://api2.watttime.org/index'
        self.username = environ.get('WATTTIME_USERNAME')
        self.password = environ.get('WATTTIME_PASSWORD')
        self.http = urllib3.PoolManager()

    def get_watttime_api_token(self):
        basic_auth_headers = urllib3.make_headers(basic_auth='{}:{}'.format(self.username, self.password))
        token = self.http.request('GET', self.login_url, headers=basic_auth_headers)
        self.token = json.loads(token.data)['token']

    def get_watttime_index(self, ba_code):
        # Refresh token
        self.get_watttime_api_token()
        resp = self.http.request('GET', self.index_url, headers={'Authorization': 'Bearer {}'.format(self.token)}, fields={'ba': ba_code})
        return resp.data

class PubSub:
    def __init__(self, topic_path):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = topic_path

    def publish_message(self, data):
        # Call future.result() to wait for message to publish, or raise an exception
        print(f"Publishing message to: {self.topic_path}")
        print(data)
        self.publisher.publish(self.topic_path, data).result()
