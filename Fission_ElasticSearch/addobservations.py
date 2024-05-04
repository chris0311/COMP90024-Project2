import logging, json
from flask import current_app, request
from elasticsearch8 import Elasticsearch

def main():
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=('elastic', 'elastic')
    )

    current_app.logger.info(f'Observations to add:  {request.get_json(force=True)}')

    for obs in request.get_json(force=True):
        res = client.index(
            index='observations',
            body=obs
        )
        current_app.logger.info("created observation")

    return 'ok'
