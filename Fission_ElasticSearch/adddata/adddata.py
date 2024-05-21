import logging
import json
from flask import Flask, current_app, request
from elasticsearch8 import Elasticsearch


def main():
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    try:
        data = request.get_json(force=True)
        eindex = request.headers.get('X-Fission-Params-Index')
        current_app.logger.info(f'Save to index: {eindex}')
        current_app.logger.info(f'Data to add: {data}')
        
        for d in data:
            try:
                res = client.index(
                    index=eindex,
                    body=d
                )
                current_app.logger.info(f"Sent to ES: {res}")
            except Exception as es_error:
                current_app.logger.error(f"Error sending to ES: {es_error}")
        
        return 'ok'
    except Exception as e:
        current_app.logger.error(f"Error processing request: {e}")
        return 'No data found in headers', 500