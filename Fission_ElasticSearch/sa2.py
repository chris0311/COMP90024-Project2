import logging
import json
from flask import Flask, current_app, request, Response
from elasticsearch8 import Elasticsearch
from string import Template


def main():
    query_template = Template('''
    {
        "query": {
            "terms": {
                "SA2_CODE21": ${sa2_codes}
            }
        },
        "_source": ["median_age"]
    }''')

    try:
        sa2_codes = request.get_json(force=True)
    except Exception as e:
        return 'Error when processing request', 500

    query = query_template.substitute(sa2_code=sa2_codes)

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

    hits = res['hits']['hits']

    # Collect all median_age values from the hits
    median_ages = []
    for hit in hits:
        try:
            median_age = hit['_source']['median_age']
            median_ages.append(median_age)
        except KeyError:
            return 'No median_age found in response', 500

    # Check if there are no results
    if not median_ages:
        return 'No results found', 200


    return json.dumps(median_ages)

