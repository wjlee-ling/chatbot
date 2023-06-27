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
        sst.ans = match_reply.group(0).replace(r"\n", "\n")
        if match_url:= re.search(pattern_url, text):
            sst.ans += f"\n{match_url.group(0)}"
    else:
        sst.ans = "다시 ENTER를 눌러주세요"

st.title("경기청년 갭이어 프로그램 FAQ")

user_input = st.text_input(label="챗봇에게 물어보기👇", key="user_input", on_change=get_response)

with st.expander("이런 건 안 궁금하세요?", expanded=True):
    st.markdown("""
    * 이 챗봇은 뭔가요?
    * 경기청년 갭이어 프로그램이 뭔가요?
    * 직장인도 갭이어 프로그램에 지원 가능한가요?
    * 저도 지원할 수 있나요?
    * 갭이어 선정 과정은요?
    * 면접 질문은?
    """)

if "ans" in sst:
    col1, col2 = st.columns(2)
    with col1:
        st.success(sst.ans)
    with col2:
        st.image("https://github.com/boostcampaitech4lv23nlp2/final-project-level3-nlp-13/assets/61496071/3c7b10ff-5bc5-4006-8400-d234df523c46", caption="저는 시아예요")

if "json" in sst:
    with st.expander("More info"): 
        st.write(sst.json)