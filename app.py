import streamlit as st
from chatbot import Chatbot, KB

# initialize bot
bot = Chatbot(kb=KB, threshold=0.2)
bot.fit()

st.title("Aqmer Chatbot")

# session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# display chat history
for message in st.session_state.chat_history:
    user_msg = message["user"]
    bot_msg = message["bot"]

    # User message
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: flex-end;
            margin: 6px 0;
        ">
            <div style="
                background-color: #0B93F6;
                color: white;
                padding: 10px 14px;
                border-radius: 12px;
                max-width: 70%;
                word-wrap: break-word;
            ">
                {user_msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Bot message
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: flex-start;
            margin: 6px 0;
        ">
            <div style="
                background-color: #E5E5EA;
                color: black;
                padding: 10px 14px;
                border-radius: 12px;
                max-width: 70%;
                word-wrap: break-word;
            ">
                {bot_msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# input field
def submit():
    reply, top_matches = bot.reply(st.session_state.input_text)
    st.session_state.chat_history.append({
        "user": st.session_state.input_text,
        "bot": reply
    })
    st.session_state.input_text = ""  # clear input

st.text_input("Type your message:", key="input_text", on_change=submit)

# show top matches for last message
if st.session_state.chat_history:
    last_message = st.session_state.chat_history[-1]
    reply, top_matches = bot.reply(last_message["user"])
    with st.expander("Top matches & scores"):
        for txt, score in top_matches:
            st.write(f"- {txt} — {score:.3f}")
