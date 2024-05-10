from flask import current_app, request
from mastodon import Mastodon
import requests
import json, time


def main():
    try:
        date = request.headers.get('X-Fission-Params-Date')
        year = date[:4]
        month = date[4:6]
        day = date[6:8]
        hour = date[8:10]
        minute = date[10:12]
        second = date[12:14]
        return f'{year}-{month}-{day}T{hour}:{minute}:{second}Z'
    except Exception as e:
        return "No date found in headers: " + str(e)
