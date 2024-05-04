(
  cd fission
  fission function create --name wharvester --spec --env python --code ./functions/wharvester.py
)

(
  cd ./fission/functions/enqueue
  zip -r enqueue.zip .
  mv enqueue.zip ../
)

(
  cd fission
  fission package create --spec --sourcearchive ./functions/enqueue.zip \
    --env python \
    --name enqueue \
    --buildcmd './build.sh'

  fission function create --spec --name enqueue \
    --pkg enqueue \
    --env python \
    --entrypoint "enqueue.main"
)

(
  cd fission/functions/addobservations
  zip -r addobservations.zip .
  mv addobservations.zip ../
)

(
  cd fission
  fission package create --sourcearchive ./functions/addobservations.zip\
    --spec\
    --env python\
    --name addobservations\
    --buildcmd './build.sh'

  fission fn create --name addobservations\
    --spec\
    --pkg addobservations\
    --env python\
    --entrypoint "addobservations.main" # Function name and entrypoint
)
