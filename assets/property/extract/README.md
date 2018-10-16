# aemigrate - Extract Asset Properties 
## Adobe Experience Manager (AEM) solution
## Author: Ashokkumar T A								
## Date: 15-Oct-2018

Extracts the configured set of asset properties and writes it to a CSV file.   

## Configuration to change
```
cq_host - Host name of the AEM instance to connect to 
cq_port - Port number of the AEM instance
cq_user - User ID to connect to the AEM Instance	
cq_password - Password of the AEM User ID
path_list - List of dam path under which to check and find all assets to extract
extract_properties - List of properties to extract
```



## Other key configuration entries

The current configuration has the right entries for these properties. These properties might need to be changed depending on the scenario. Following are such properties:
```
properties_output - The output CSV file path to store the extracted properties
```

## Input files
```
path_list - List of dam path under which to check and find all assets to extract
```

## Output files
```
properties_output - The output CSV file path to store the extracted properties 
```

## How to run
After the correct configurations are done and input files placed in the folder, run the script xap.py by executing the below command under this script folder
```
python xap.py 
```

---
> Environment Tested on:  AEM6.2, Python 2.7.15 
