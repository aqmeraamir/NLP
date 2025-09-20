# app.py (Streamlit)
import streamlit as st
from chatbot import Chatbot, KB  # assume same directory and code refactored to import


bot = Chatbot(kb=KB)
bot.fit()

st.title("Embeddings Chatbot demo")
q = st.text_input("Ask something")
if q:
    reply, top = bot.reply(q)
    st.write("**Bot:**", reply)
    st.write("**Top matches:**")
    for txt, score in top:
        st.write(f"- {txt} — {score:.3f}")