from flask import request, current_app
from textblob import TextBlob

def main():
    try :
        text = request.headers.get('X-Fission-Params-Text')
        blob = TextBlob(text)
        current_app.logger.info(f'Sentiment analysis done on {text}')
        return blob.sentiment.polarity
    except :
        return 'No text found in headers'