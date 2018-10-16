# aemigrate - Fetch Assets 
## Adobe Experience Manager (AEM) solution
## Author: Ashokkumar T A								
## Date: 15-Oct-2018

Fetch Assets - Probes and finds all the assets under a given path and writes the list of assets found, to the configured output file

## Configuration to change
```
cq_host - Host name of the AEM instance to connect to 
cq_port - Port number of the AEM instance
cq_user - User ID to connect to the AEM Instance	
cq_password - Password of the AEM User ID
assets_in_path - DAM path under which to check and find all assets under it 
```


### Other key configuration entries
The current configuration has the right entries for these properties. These properties might need to be changed depending on the scenario. Following are such properties:
```
assets_file - The output file path that stores the list of assets found
```

## Input files
None

## Output files
```
assets_file - Default configured to output/asset_list.lst contains the list of assets found
```

## How to run
After the correct configurations are done and input files placed in the folder, run the script fa.py by executing the below command under this script folder
```
python fa.py 
```

---
> Environment Tested on:  AEM6.2, Python 2.7.15 
