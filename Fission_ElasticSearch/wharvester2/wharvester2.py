import logging, json, requests, socket
from flask import current_app, request
from elasticsearch8 import Elasticsearch

def reformat_date(date):
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[8:10]
    minute = date[10:12]
    second = date[12:14]
    return f'{year}-{month}-{day}T{hour}:{minute}:{second}Z'


def main():
    data = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()
    extracted_field = data['observations']['data'][0]
    extracted_data = {
        'air_temp': float(extracted_field['air_temp']),
        'apparent_t': float(extracted_field['apparent_t']),
        'rain_trace': float(extracted_field['rain_trace']),
        'rel_hum': float(extracted_field['rel_hum']),
        'vis_km': int(extracted_field['vis_km']),
        'wind_spd_kmh': int(extracted_field['wind_spd_kmh']),
        'local_date_time': reformat_date(data['observations']['data'][1]['local_date_time_full']),
    }

    current_app.logger.info(f'Harvested one weather observation')
    # requests.post(url='http://router.fission/enqueue/observations',
    #     headers={'Content-Type': 'application/json'},
    #     data=json.dumps(extracted_data)
    # )

    # Add the harvested data to the Elasticsearch cluster
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=('elastic', 'elastic')
    )

    res = client.index(
        index='observations',
        body=extracted_data
    )
    current_app.logger.info("created observation")

    return 'OK'