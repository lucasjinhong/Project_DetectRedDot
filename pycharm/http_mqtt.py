import requests
import json
import paho.mqtt.client as mqtt


class send_http:
    def __init__(self, url, payload):
        self.url = url
        self.payload = payload

    def http_request(self):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(self.url, json.dumps(self.payload), headers=headers)
        print(f"Status Code: {r.status_code}, Response: {r.json()}")
