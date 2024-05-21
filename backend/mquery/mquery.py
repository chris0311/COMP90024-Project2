import logging
import json
from flask import Flask, current_app, request
from elasticsearch8 import Elasticsearch
from string import Template


def main():
    days_expr= Template('''{
                    "range": {
                        "created_at": {
                            "gte": "${sdate}T00:00:00",
                            "lte": "${edate}T23:59:59"
                        }
                    }
                }''')

    query_template = Template('''{
        "query": ${days_expr},
        "size": ${size}
    }''')

    try:
        start_date = request.headers.get('X-Fission-Params-Sdate')
        end_date = request.headers.get('X-Fission-Params-Edate')
        size = request.args.get('size', default=20, type=int)
        current_app.logger.info(f'querying {start_date} to {end_date}')

        days_expr = days_expr.substitute(sdate=start_date, edate=end_date)
        query = query_template.substitute(days_expr=days_expr, size=size)

        client = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            ssl_show_warn=False,
            basic_auth=('elastic', 'elastic')
        )

        res = client.search(
            index = 'mastodon',
            body = json.loads(query)
        )

        res_dict = res.body

        return json.dumps(res_dict)
        
    except KeyError as e:
        current_app.logger.error(f"Error processing request: {e}")
        return 'No data found in headers', 500
    except Exception as e:
        current_app.logger.error(f"Error processing request: {e}")
        return 'No data found in headers', 500
