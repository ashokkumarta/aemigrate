# aemigrate - Download assets from AEM 

Downloads the assets from AEM and stores it in the local folder.   

## Configuration to change
```
DOWNLOAD_LIST - List of assets to be downloaded. This file should contain the full URL path of the assets to be downloaded, one asset per line 
DOWNLOAD_PATH - Path to which the assets are downloaded to	
DOWNLOAD_LOG - Path where the log files are written
```


## Input files
```
DOWNLOAD_LIST - List of assets to be downloaded. This file should contain the full URL path of the assets to be downloaded, one asset per line
```

## Output files
```
DOWNLOAD_PATH - All the assets downloaded are stored under this path 
```

## How to run
After the correct configurations are done and input files placed in the folder, run the script download.sh by executing the below command under this script folder
```
./download.sh 
```

---
> Environment Tested on:  AEM6.2, RHEL5 
