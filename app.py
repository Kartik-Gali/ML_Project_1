import streamlit as st
import requests
import json  # Import JSON module for formatting

st.title("📢 News Summarization & Sentiment Analysis")

# Initialize session state variables
if "news_fetched" not in st.session_state:
    st.session_state.news_fetched = False
if "articles" not in st.session_state:
    st.session_state.articles = []
if "audio_generated" not in st.session_state:
    st.session_state.audio_generated = False
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

company = st.text_input("Enter a company name")

if st.button("Fetch News"):
    response = requests.get(f'http://127.0.0.1:5000/fetch-news?company={company}')
    
    if response.status_code == 200:
        data = response.json()
        st.session_state.articles = data["articles"]
        st.session_state.news_fetched = True  # Set news fetched to True

if st.session_state.news_fetched:
    st.subheader("News Articles in JSON Format")
    
    # Display the raw JSON response
    st.json(st.session_state.articles)  # Displays structured JSON output

    if st.button("Generate Hindi Audio") and not st.session_state.audio_generated:
        summary_text = " ".join([article['summary'] for article in st.session_state.articles if article['summary']])
        
        print(f"📤 Sending text to Flask: '{summary_text}'")  # Debugging print

        tts_response = requests.post('http://127.0.0.1:5000/generate-tts', json={'text': summary_text})

        if tts_response.status_code == 200:
            with open("tts_output.mp3", "wb") as f:
                f.write(tts_response.content)

            st.session_state.audio_generated = True
            st.session_state.audio_file = "tts_output.mp3"

if st.session_state.audio_generated and st.session_state.audio_file:
    st.audio(st.session_state.audio_file)

    with open(st.session_state.audio_file, "rb") as f:
        st.download_button(label="Download Audio", data=f, file_name="news_audio.mp3", mime="audio/mpeg")
