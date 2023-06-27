import time
import re
import streamlit as st
from streamlit import session_state as sst
from agent import ChatbotMessageSender

def get_response():
    sst.json = ""
    sst.ans = ""
    res = ChatbotMessageSender().req_message_send(sst.user_input)
    print(f"Response code: {res.status_code}")

    if res.status_code == 200:
        with st.spinner(text="답변을 생성하고 있어요"):
            time.sleep(0.8)
        sst.json = res.text
        print(res.text)
        parse(sst.json)
        # json_obj = res.json() 
        # sst.ans = json_obj["bubbles"][0] #["data"]["cover"]["data"]["description"]

def parse(text):
    pattern_reply = re.compile(r'(?<="data":{"description":").+?(?="})')
    pattern_url = re.compile(r'(?<={"url":").+?(?="})')
    match_reply = re.search(pattern_reply, text)
    if match_reply:
        sst.ans = match_reply.group(0)
        if match_url:= re.search(pattern_url, text):
            sst.ans += f"\n{match_url.group(0)}"
    else:
        sst.ans = "다시 submit 버튼을 눌러주세요"

st.title("경기청년 갭이어 프로그램 FAQ")
user_input = st.text_input(label='무엇이 궁금하세요?', key="user_input", on_change=get_response)

if "ans" in sst:
    col1, col2 = st.columns(2)
    with col1:
        st.success(sst.ans)
    with col2:
        st.image("https://github.com/boostcampaitech4lv23nlp2/final-project-level3-nlp-13/assets/61496071/3c7b10ff-5bc5-4006-8400-d234df523c46")

if "json" in sst:
    with st.expander("More info"): 
        st.write(sst.json)