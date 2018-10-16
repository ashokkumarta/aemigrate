# aemigrate - Update Asset Properties 
## Adobe Experience Manager (AEM) solution
## Author: Ashokkumar T A								
## Date: 15-Oct-2018

This script updates the properties for the given set of assets based on the input CSV data

## Configuration to change
```
cq_host - Host name of the AEM instance to connect to 
cq_port - Port number of the AEM instance
cq_user - User ID to connect to the AEM Instance	
cq_password - Password of the AEM User ID
base_path - DAM base path under which update is done for the assets
update_properties - List of properties of the assets that needs to be updated
```

## Other key configuration entries
The current configuration has the right entries for these properties. These properties might need to be changed depending on scenario. Following are such properties:
```
extract_properties - List of legacy properties to extract and log before the update starts
```

## Input files
```
assets_to_update.csv - Input CSV file based on which the asset properties are updated. The header row is the name of the property to be updated and the second row is the property type. The first column has to be the path of the asset - the property jcr:path.
```

## Output files
```
output/successful_assets.lst - List of assets for which the migration is successful
output/failed_assets.lst - List of assets for which the migration has failed
output/skipped_assets.lst - List of assets for which the migration is skipped
```

## How to run

Before starting the batch run, ensure
1. Correct configurations are done in the configuration file 
2. Input files placed in the input folder
3. Output and log folders containing data of the previous run are backed up (if needed) and contents of these folders cleared (The scripts cl.sh & cl.bat deletes the files in logs and out folders on linux & windows environments respectively. Pls. make sure to run this script only after taking the necessory backups) 

After the above points are checked, run the script uap.py by executing the below command under this script folder
```
python uap.py 
```

## Checking the status of the run
The progress and the status summary of the migration run is displayed on the console. 
Detailed logging is also done to check and validate the migration. 
The following files has migration run details

```
logs/status.log - Overall summary of the migration run
logs/trace.log - Detaied track on the migration run, including the details of the properties migrated/set for each asset
logs/error.log - Error details about the migration failures

out/successful_assets.lst - List of assets for which the update is successful
out/failed_assets.lst - List of assets for which the update has failed
out/skipped_assets.lst - List of assets for which the update is skipped
out/properties_before_migration.csv - CSV dump of the property values before the migration. 
```

---
> Environment Tested on:  AEM6.2, Python 2.7.15 
