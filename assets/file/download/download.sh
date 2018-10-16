. cfg/run_config.sh

xargs -n 1 wget -x -nH -P $DOWNLOAD_PATH -S --tries=2 < $DOWNLOAD_LIST > $DOWNLOAD_LOG
