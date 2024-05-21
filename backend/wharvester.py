import logging, json, requests, socket
from flask import current_app, request


def main():
    data = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()
    extracted_field = data['observations']['data'][0]
    date = data['observations']['data'][1]['local_date_time_full']
    reformatted_date = requests.post(
        url=f"http://router.fission/redate",
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'date': date})
    )
    extracted_data = {
        'air_temp': float(extracted_field['air_temp']),
        'apparent_t': float(extracted_field['apparent_t']),
        'rain_trace': float(extracted_field['rain_trace']),
        'rel_hum': float(extracted_field['rel_hum']),
        'vis_km': int(extracted_field['vis_km']),
        'wind_spd_kmh': int(extracted_field['wind_spd_kmh']),
        'local_date_time': reformatted_date.text,
    }

    res = []
    res.append(extracted_data)

    current_app.logger.info(f'Harvested one weather observation, saving to ElasticSearch')
    requests.post(url='http://router.fission/adddata/observations',
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(res))
    current_app.logger.info("added observation")

    return 'OK'
