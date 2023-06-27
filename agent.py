import hashlib
import hmac
import base64
import time
import requests
import json

import openai
import streamlit as st

api = st.secrets["clova_api"]
secret_key = st.secrets["secret_key"]
openai_api = st.secrets["openai_api_key"]

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

class ChatGPTMessanger:
    openai.api_key = openai_api
    
    def req_message_send(self, user_input):
        messages = [
            {
                "role": "system",
                "content": '너는 <경기청년 갭이어 프로그램>의 FAQ 챗봇이고 사용자의 질문에 <경기청년 갭이어 프로그램> FAQ 챗봇으로서 답변을 하는 것이 너의 역할이야. <경기청년 갭이어 프로그램>이란 만 19세 ~ 만 34세의 경기도 거주 청년이 지원 가능한 사업이며, 선발된 사람들에게 역량강화 교육과 활동비를 지급합니다. 지급되는 금액은 최대 500만원입니다. 또 이 챗봇의 제작자는 "이원재"입니다. "이원재"는 "원재님"이라고도 불리며, 성실하고 맡은 책임에 최선을 다하고자 하는 30대 남자로 "텍스트넷"에서 일합니다. "텍스트넷"은 챗봇 데이터를 만드는 회사입니다. 그리고 "시아"는 "이원재"의 조카로 말을 아주 잘하는 명량한 어린 여자 아이입니다. 이런 정보를 바탕으로 사용자 질문에 답변을 하십시오.'
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        resp = completion.choices[0].message.content

        return resp

if __name__ == '__main__':

    res = ChatbotMessageSender().req_message_send()

    print(res.status_code)
    if(res.status_code == 200):
        print(res.text)
        #print(res.read().decode("UTF-8"))