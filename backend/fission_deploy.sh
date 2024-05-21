( 
cd ./fission/functions/scale
zip -r scale.zip .
mv scale.zip ../
)


(
  cd fission
  fission package create --sourcearchive ./functions/scale.zip \
    --env python-39x \
    --name scale\
    --buildcmd './build.sh'
)

(
  fission function create --name scale\
    --pkg scale \
    --env python-39x \
    --fntimeout 600 \
    --entrypoint "scale.main"
)

fission httptrigger create --name mredate --url "/mredate" --method POST --function mredate

fission timer create --name mharvester --function mharvester --cron "@every 3m"

fission function update --name genloc --env python --code ./fission/functions/genloc.py

fission httptrigger create --name mquery --url "/mquery/{sdate:[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]}/{edate:[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]}" --method GET --function mquery