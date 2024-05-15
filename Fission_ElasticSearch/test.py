from flask import current_app, request
import requests
import json


def main():
    res = requests.post(url='http://router.fission/sentiment/',
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps({'date': "2024-05-15 05:12:05+00:00"}))

    return res
