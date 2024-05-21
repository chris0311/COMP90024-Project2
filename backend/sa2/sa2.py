import logging
import json
from flask import Flask, current_app, request
from elasticsearch8 import Elasticsearch
from string import Template


def main():
    query_template = Template('''
    {
        "query": {
        "match": {
            "SA2_CODE21": "${sa2_code}"
        }
    },
    "_source": ["median_age"]
    }''')

    try:
        sa2_code = request.headers.get('X-Fission-Params-Sa2code')
        current_app.logger.info(f'querying {sa2_code}')
    except KeyError as e:
        current_app.logger.error(f"Error processing request: {e}")
        return 'No data found in headers', 500

    query = query_template.substitute(sa2_code=sa2_code)

    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    res = client.search(
        index='sa2',
        body=json.loads(query)
    )

    res = res.body
    try:
        result = res['hits']['hits'][0]['_source']['median_age']
    except IndexError as e:
        return 'No results found', 200
    
    return str(result)

