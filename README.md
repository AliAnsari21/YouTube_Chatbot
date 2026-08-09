# YouTube Chatbot 🎥

This is a simple AI chatbot that allows users to ask questions about a YouTube video.

### Features

* Extracts the YouTube video transcript.
* Splits the transcript into smaller chunks.
* Uses Hugging Face embeddings and FAISS for searching.
* Uses Groq LLM to generate answers.
* Built using Streamlit.

### Technologies

Python, Streamlit, LangChain, FAISS, Hugging Face, Groq

### How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Enter the YouTube Video ID, ask a question, and the chatbot will generate an answer based on the video transcript.
