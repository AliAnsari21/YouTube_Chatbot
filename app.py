import streamlit as st
from chatbot import create_conversational_chain

st.title("🎥 YouTube Chatbot")

api_key = st.text_input("Groq API Key",type="password")

video_id = st.text_input("YouTube Video ID")

question = st.text_input("Ask a question")

if st.button("Ask"):

    if not api_key:
        st.error("Enter Groq API key")

    elif not video_id:
        st.error("Enter YouTube Video ID")

    elif not question:
        st.error("Enter a question")

    else:

        try:

            with st.spinner("Processing..."):

                answer = create_conversational_chain(
                    video_id,
                    api_key,
                    question
                )

            st.subheader("🤖 Answer")

            st.write(answer)

        except Exception as e:

            st.error("Something went wrong")

            st.exception(e)

