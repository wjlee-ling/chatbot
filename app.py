import re
import streamlit as st
from streamlit import session_state as sst
from agent import ChatbotMessageSender


def get_response():
    p = re.compile(r'(?<="data":{"description":).+(?=},"information")')
    if "user_input" in sst:
        res = ChatbotMessageSender().req_message_send(sst.user_input)
        if(res.status_code == 200):
            print(res.text)
            if re.findall(p, res.text):
                sst.ans = re.findall(p, res.text)[0] 
        

st.title("경기청년 갭이어 프로그램 FAQ")
with st.form(key='my_form'):
	sst.user_input = st.text_input(label='무엇이 궁금하세요?')
	submit_button = st.form_submit_button(label='Submit', on_click=get_response)

if "ans" in sst:
    # st.write(type(sst.ans))
    st.success(sst.ans)