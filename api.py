from flask import Flask, request, jsonify, send_file
import os
from utils import fetch_news, analyze_sentiment, extract_topics, generate_hindi_audio

app = Flask(__name__)

@app.route('/fetch-news', methods=['GET'])
def get_news():
    company = request.args.get('company', '')
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    articles = fetch_news(company)
    for article in articles:
        article['sentiment'] = analyze_sentiment(article['summary'])
        article['topics'] = extract_topics(article['summary'])

    return jsonify({"articles": articles})


@app.route('/generate-tts', methods=['POST'])
def generate_tts():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    audio_file = generate_hindi_audio(text)

    if audio_file and os.path.exists(audio_file):
        return send_file(audio_file, as_attachment=True, mimetype="audio/mpeg")
    else:
        return jsonify({'error': 'TTS conversion failed'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
