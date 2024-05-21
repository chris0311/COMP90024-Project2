from flask import current_app, request
import requests
import json, time


def main():
    try:
        data = request.get_json(force=True)
        date = data['date']
        year = date[:4]
        month = date[4:6]
        day = date[6:8]
        hour = date[8:10]
        minute = date[10:12]
        second = date[12:14]
        return f'{year}-{month}-{day}T{hour}:{minute}:{second}Z'
    except Exception as e:
        return "No date found in headers: " + str(e)
