from flask import request, current_app
from textblob import TextBlob

def main():
    try:
        current_app.logger.info('requesting sentiment analysis')
        data = request.get_json(force=True)
        text = data['text']
        blob = TextBlob(text)
        current_app.logger.info(f'Sentiment analysis done on {text}')
        return str(blob.sentiment.polarity)  # Ensure returning a string
    except Exception as e:
        current_app.logger.error(f'Error: {e}')
        return 'No text found in request'
