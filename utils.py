import requests
import gtts
import os
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from keybert import KeyBERT
import spacy

# Load spaCy and KeyBERT models
nlp = spacy.load("en_core_web_sm")
kw_model = KeyBERT()
analyzer = SentimentIntensityAnalyzer()
translator = Translator()

NEWS_API_KEY = "1b6e9827d0c74adb8afe6e09d15e9912"  # Replace with your API key

def fetch_news(company):
    """Fetch news articles related to a company."""
    url = f"https://newsapi.org/v2/everything?q={company}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    articles = data.get("articles", [])[:10]
    
    news_list = []
    for article in articles:
        title = article.get("title", "No Title")
        summary = article.get("description", "No Summary")
        news_list.append({"title": title, "summary": summary})

    return news_list


def analyze_sentiment(text):
    """Analyze sentiment (positive, negative, neutral) of a given text."""
    scores = analyzer.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return 'Positive'
    elif scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


def extract_topics(text):
    """Extract key topics using KeyBERT."""
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=3)
    return [kw[0] for kw in keywords] if keywords else ["No Topics"]


def generate_hindi_audio(text):
    """Translate text to Hindi and generate speech."""
    try:
        translated_text = translator.translate(text, src="en", dest="hi").text
        tts = gtts.gTTS(translated_text, lang='hi')
        audio_file = "tts_output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None
