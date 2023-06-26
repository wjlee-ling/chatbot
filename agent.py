import hashlib
import hmac
import base64
import time
import requests
import json

import streamlit as st

api = st.secrets["clova_api"]
secret_key = st.secrets["secret_key"]

class ChatbotMessageSender:

    # chatbot api gateway url
    ep_path = api
    # chatbot custom secret key
    secret_key = secret_key

    def req_message_send(self, user_question):

        timestamp = self.get_timestamp()
        request_body = {
            'version': 'v2',
            'userId': 'oianadministrator9123',
            'timestamp': timestamp,
            'bubbles': [
                {
                    'type': 'text',
                    'data': {
                        'description': user_question
                    }
                }
            ],
            'event': 'send'
        }

        ## Request body
        encode_request_body = json.dumps(request_body).encode('UTF-8')

        ## make signature
        signature = self.make_signature(self.secret_key, encode_request_body)

        ## headers
        custom_headers = {
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-CHATBOT_SIGNATURE': signature
        }

        # print("## Timestamp : ", timestamp)
        # print("## Signature : ", signature)
        # print("## headers ", custom_headers)
        # print("## Request Body : ", encode_request_body)

        ## POST Request
        response = requests.post(headers=custom_headers, url=self.ep_path, data=encode_request_body)

        return response

    @staticmethod
    def get_timestamp():
        timestamp = int(time.time() * 1000)
        return timestamp

    @staticmethod
    def make_signature(secret_key, request_body):

        secret_key_bytes = bytes(secret_key, 'UTF-8')

        signing_key = base64.b64encode(hmac.new(secret_key_bytes, request_body, digestmod=hashlib.sha256).digest())

        return signing_key


if __name__ == '__main__':

    res = ChatbotMessageSender().req_message_send()

    print(res.status_code)
    if(res.status_code == 200):
        print(res.text)
        #print(res.read().decode("UTF-8"))