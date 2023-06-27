import time
import re
import streamlit as st
from streamlit import session_state as sst
from agent import ChatbotMessageSender,ChatGPTMessanger


@st.cache_resource
def init_clova_bot():
    sst.clova_bot = ChatbotMessageSender()

@st.cache_resource
def init_chatgpt_bot():
    sst.ChatGPT_bot = ChatGPTMessanger()

def get_response():
    init_clova_bot()
    sst.json = ""
    sst.ans = ""
    res = sst.clova_bot.req_message_send(sst.user_input)
    print(f"Response code: {res.status_code}")

    if res.status_code == 200:
        with st.spinner(text="답변을 생성하고 있어요"):
            time.sleep(0.8)
        sst.json = res.text
        print(res.text)
        parse(sst.json)
        # json_obj = res.json() 
        # sst.ans = json_obj["bubbles"][0] #["data"]["cover"]["data"]["description"]

def get_chatgpt_response():
    init_chatgpt_bot()
    sst.chatgpt_ans = sst.ChatGPT_bot.req_message_send(sst.user_input)
    sst.json = ""
    
def parse(text):
    pattern_fallback = re.compile("❌해당 질문에 대한 시나리오를 구성하지 못했습니다.")
    pattern_reply = re.compile(r'(?<="data":{"description":").+?(?="})')
    pattern_url = re.compile(r'(?<={"url":").+?(?="})')
    match_reply = re.search(pattern_reply, text)

    sst.is_fallback = True if re.search(pattern_fallback, text) else False

    if match_reply:
        sst.ans = match_reply.group(0).replace(r"\n", "\n").replace('"","url":"', ' ')
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
        if "is_fallback" in sst and sst.is_fallback:
            st.warning(f"질문을 제대로 이해하지 못했어요. 대신 ChatGPT🤖가 답변 드려도 될까요? (답변에 시간이 좀 걸려요)")
            if st.button(label="ChatGPT🤖의 답변 보기", on_click=get_chatgpt_response):
                if "chatgpt_ans" in sst:
                    st.success(sst.chatgpt_ans)
        else:
            st.success(sst.ans)

    with col2:
        if "is_fallback" in sst and sst.is_fallback:
            st.image("https://github.com/wjlee-ling/algorithms/assets/61496071/48c2e677-e122-4667-80c7-5315d527540f", width=130, caption="삼촌이 아직 많이 부족해요ㅠ")
        else:
            st.image("https://github.com/boostcampaitech4lv23nlp2/final-project-level3-nlp-13/assets/61496071/3c7b10ff-5bc5-4006-8400-d234df523c46", width=130, caption="저는 시아예요")

# if "json" in sst:
#     with st.expander("More info"): 
#         st.write(sst.json)