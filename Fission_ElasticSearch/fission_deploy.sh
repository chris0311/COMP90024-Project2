( 
cd ./fission/functions/concat
zip -r concat.zip .
mv concat.zip ../
)


(
  cd fission
  fission package create --sourcearchive ./functions/concat.zip \
    --env python-39 \
    --name concat\
    --buildcmd './build.sh'
)

(
  fission function create --name concat\
    --pkg concat\
    --env python-39 \
    --fntimeout 600 \
    --entrypoint "concat.main"
)

fission httptrigger create --name mredate --url "/mredate" --method POST --function mredate

fission timer create --name mharvester --function mharvester --cron "@every 3m"

fission function update --name genloc --env python --code ./fission/functions/genloc.py

fission httptrigger create --name mquery --url "/mquery/{sdate:[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]}/{edate:[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]}" --method GET --function mquery