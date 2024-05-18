import logging
import json
import requests
from flask import Flask, current_app, request
import pandas as pd


def round_to_nearest_half_hour(dt):
    minute = dt.minute
    if minute < 15:
        return dt.replace(minute=0, second=0)
    elif minute < 45:
        return dt.replace(minute=30, second=0)
    else:
        return dt.replace(minute=0, second=0) + pd.Timedelta(hours=1)


def main():
    try:
        start_date = request.headers.get('X-Fission-Params-Sdate')
        end_date = request.headers.get('X-Fission-Params-Edate')
        current_app.logger.info(f'querying {start_date} to {end_date}')
        size = request.args.get('size', default=20, type=int)
        msize = request.args.get('msize', default=20, type=int)
        bsize = request.args.get('bsize', default=20, type=int)

        bom_res = requests.get(url=f'http://router.fission/bomquery/{start_date}/{end_date}?size={bsize}')
        mastodon_res = requests.get(url=f'http://router.fission/mquery/{start_date}/{end_date}?size={msize}')

        bom_hit = bom_res.json()['hits']['hits']
        mastodon_hit = mastodon_res.json()['hits']['hits']

        bom_data = []
        for hit in bom_hit:
            bom_data.append(hit['_source'])
        
        mastodon_data = []
        for hit in mastodon_hit:
            mastodon_data.append(hit['_source'])

        current_app.logger.info(f"harvested {len(bom_data)} bom data and {len(mastodon_data)} mastodon data")

        bom_df = pd.DataFrame(bom_data)
        mastodon_df = pd.DataFrame(mastodon_data)

        # separate mastodon_df's location
        mastodon_df['lat'] = mastodon_df['location'].apply(lambda x: x['lat'])
        mastodon_df['lon'] = mastodon_df['location'].apply(lambda x: x['lon'])

        # drop location column
        mastodon_df.drop('location', axis=1, inplace=True)

        # merge bom_df and mastodon_df
        mastodon_df['rounded_created_at'] = pd.to_datetime(mastodon_df['created_at'])
        mastodon_df['rounded_created_at'] = mastodon_df['rounded_created_at'].apply(round_to_nearest_half_hour)
        mastodon_df['rounded_created_at'] = mastodon_df['rounded_created_at'].dt.tz_localize(None)

        bom_df['rounded_local_date_time'] = pd.to_datetime(bom_df['local_date_time'])
        bom_df['rounded_local_date_time'] = bom_df['rounded_local_date_time'].apply(round_to_nearest_half_hour)
        bom_df['rounded_local_date_time'] = bom_df['rounded_local_date_time'].dt.tz_localize(None)

        current_app.logger.debug(f"mastodon_df['rounded_created_at']: {mastodon_df.iloc[0]['rounded_created_at']}")
        current_app.logger.debug(f"bom_df['rounded_local_date_time']: {bom_df.iloc[0]['rounded_local_date_time']}")

        merged_df = pd.merge(mastodon_df, bom_df, left_on='rounded_created_at', right_on='rounded_local_date_time', how='inner')
        
        # only return #size rows
        merged_df = merged_df.head(size)

        return merged_df.to_json(orient='records', date_format='iso')
    
    except KeyError as e:
        current_app.logger.error(f"Error processing request: {e}")
        return 'No data found in headers', 500
    
    except Exception as e:
        current_app.logger.error(f"Error processing request: {e}")
        return 'Error processing request', 500