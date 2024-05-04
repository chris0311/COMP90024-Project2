(
  cd fission
  fission timer create --spec --name weather-ingest --function wharvester --cron "@every 30m"

  fission httptrigger create --spec --name enqueue --url "/enqueue/{topic}" --method POST --function enqueue

  fission mqtrigger create --name add-observations \
    --spec\
    --function addobservations \
    --mqtype kafka \
    --mqtkind keda \
    --topic weather \
    --errortopic errors \
    --maxretries 3 \
    --metadata bootstrapServers=my-cluster-kafka-bootstrap.kafka.svc:9092 \
    --metadata consumerGroup=my-group \
    --cooldownperiod=30 \
    --pollinginterval=5
)
