# aemigrate - Create tags 

This script creates the tags provided in a mapping file. For each of the new tag defined in the mapping sheet, finds the Title & Description of the corresponding tags from the legacy tags extract set defined and creates
the tag in the configured AEM instance


## Configuration to change
```
cq_host - Host name of the AEM instance to connect to 
cq_port - Port number of the AEM instance
cq_user - User ID to connect to the AEM Instance	
cq_password - Password of the AEM User ID
legacy_tags_extract - List of CSV files which has the dump of the legacy tags extracted using tags extract script 
new_tags_mapping - Mapping CSV file containing the new tags to be created mapped to its corresponding legacy tag 
```


## Other key configuration entries

The current configuration has the right entries for these properties. These properties might need to be changed depending on the scenario. Following are such properties:

```
successful_tags - The output file containing the tags that are successfully created
failed_tags - The output file containing the tags for which creation failed
```

## Input files
```
legacy_tags_extract - List of CSV files which has the dump of the legacy tags extracted using tags extract script 
new_tags_mapping - Mapping CSV file containing the new tags to be created mapped to its corresponding legacy tag 
```

## Output files
```
successful_tags - The output file containing the tags that are successfully created
failed_tags - The output file containing the tags for which creation failed
```

## How to run
### After the correct configurations are done and input files placed in the folder, run the script c.py by executing the below command under this script folder

```
c.py 
```

---
> Environment Tested on:  AEM6.2, Python 2.7.15 
