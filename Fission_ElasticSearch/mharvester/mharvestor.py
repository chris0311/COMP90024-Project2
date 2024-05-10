from flask import current_app, request
from mastodon import Mastodon
import requests
import json, time

def main():
    m = Mastodon(
        api_base_url=f'https://mastodon.au'
    )

    # Get the ID of the lastid status main the public timeline
    lastid= m.timeline(timeline='public', since_id=None, limit=1, remote=True)[0]['id']

    # Sleep for 5 seconds to allow for some status to be posted before we fetch them
    time.sleep(10)

    # Fetch the statuses from the public timeline since the lastid
    # return json.dumps(m.timeline(timeline='public', since_id=lastid, remote=True), default=str)

    m_data = m.timeline(timeline='public', since_id=lastid, remote=True)

    res = []
    for data in m_data:
        content = data['content']
        content = requests.post(url='http://router.fission/mpreprocess/',
            headers={'Content-Type': 'text/plain'},
            data=content)
        sentiment = requests.post(url='http://router.fission/sentiment/',
            headers={'Content-Type': 'text/plain'},
            data=content)
        res.append({
            'created_at': data['created_at'],
            'content': content,
            'sentiment': sentiment
            }
        )

    current_app.logger.info(f'Harvested {len(res)} toots, saving to ElasticSearch')
    requests.post(url='http://router.fission/adddata/mastodon',
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(res))
    current_app.logger.info(f'Saved {len(res)} toots to ElasticSearch')

    return 'OK'
