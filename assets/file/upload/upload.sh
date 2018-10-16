. cfg/run_config.sh

ASSETS_PATH=${ASSETS_PATH}/content/dam/
find ${ASSETS_PATH}* -type d > ${UPLOAD_PATH}
sed "s|${ASSETS_PATH}||" ${UPLOAD_PATH} > ${UPLOAD_DIRS}
find ${ASSETS_PATH}* -type f > ${UPLOAD_PATH}
sed "s|${ASSETS_PATH}||" ${UPLOAD_PATH} > ${UPLOAD_FILES}

cat $UPLOAD_DIRS | xargs -n 1 -d '\n' -I % curl -v -u $UPLOAD_CQ_USER:$UPLOAD_CQ_PASSWORD -X POST -H"Content-Type: application/json" -d '{"class":"assetFolder"}'  http://$UPLOAD_CQ_HOST:$UPLOAD_CQ_PORT/api/assets/% 

cat $UPLOAD_FILES | xargs -n 1 -d '\n' sh -c 'curl -v -u $UPLOAD_CQ_USER:$UPLOAD_CQ_PASSWORD -X POST -F"name=`basename "$0"`" -F"file=@$DOWNLOAD_PATH/content/dam/$0"  http://$UPLOAD_CQ_HOST:$UPLOAD_CQ_PORT/api/assets/`dirname "$0"`/*'
