import logging
import json
from flask import Flask, current_app, request, Response
from elasticsearch8 import Elasticsearch


def main():
    try:
        sa2_codes = request.get_json(force=True)
        sa2_codes = sa2_codes['sa2_codes']
    except Exception as e:
        return 'Error when processing request', 500

    query = {
        "query": {
            "terms": {
                "SA2_CODE21": sa2_codes
            }
        }
    }

    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    query_len = len(sa2_codes)

    res = client.search(
        index='sa2',
        body=query,
        size=query_len
    )

    hits = res['hits']['hits']

    # Collect all median_age values from the hits
    median_ages = []
    for hit in hits:
        median_age = hit['_source']['median_age']
        sa2_code = hit['_source']['SA2_CODE21']
        result = {
            'SA2_CODE21': sa2_code,
            'median_age': median_age
        }
        median_ages.append(result)

    # Check if there are no results
    if not median_ages:
        return 'No results found', 200

    return json.dumps(median_ages)

