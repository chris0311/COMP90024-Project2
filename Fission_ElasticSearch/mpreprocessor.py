import json

from flask import current_app, request
import re
from bs4 import BeautifulSoup


def extract_text(html_content):
    html_content = re.sub(r'href=\S+', '', html_content)

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove elements that are meant to be invisible or are not relevant to text content
    for element in soup.find_all("span", class_="invisible"):
        element.decompose()  # This removes the element from the soup

    # Extract text from the modified HTML
    text = soup.get_text(separator=' ', strip=True)
    return text


def main():
    try:
        data = request.get_json(force=True)
        text = data['text']
        text = extract_text(text)
        current_app.logger.info(f'Extracted text from HTML')
        return text
    except:
        return 'No text found in headers'
