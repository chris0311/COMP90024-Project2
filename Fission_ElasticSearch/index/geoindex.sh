curl -XPUT -k 'https://127.0.0.1:9200/geoindex' \
   --user 'elastic:elastic' \
   --header 'Content-Type: application/json' \
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "location": {
                "type": "geo_shape"
            }
        }
    }
}'  | jq '.'
