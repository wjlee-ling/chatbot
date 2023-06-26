import re
import json
import streamlit as st
from streamlit import session_state as sst
from agent import ChatbotMessageSender


def get_response(user_input):
    # p = re.compile(r'(?<="data":{"description":).+(?=},"information")')
    # if "user_input" in sst:
    res = ChatbotMessageSender().req_message_send(user_input)
    print(f"Response code: {res.status_code}")
    if res.status_code == 200:
        json_obj = json.loads(res.text)
        sst.json = json_obj
        sst.ans = json_obj["bubbles"][0]["data"]["cover"]["data"]["description"]

        # if re.findall(p, res.text):
        #     sst.ans = re.findall(p, res.text)[0] 


st.title("경기청년 갭이어 프로그램 FAQ")
with st.form(key='my_form'):
	user_input = st.text_input(label='무엇이 궁금하세요?')
	submit_button = st.form_submit_button(label='Submit', on_click=get_response, kwargs={"user_input":user_input})

if "ans" in sst:
    # st.write(type(sst.ans))
    st.success(sst.ans)
    with st.expander("More info"): 
        st.write(sst.json)