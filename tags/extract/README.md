# aemigrate - Extract tags 

This script extracts all the tags defined under a given tag namespace.  
It probes and finds all the tags under a given tag namespace and outputs all the tags to a configured CSV file output 


## Configuration to change
```
cq_host - Host name of the AEM instance to connect to 
cq_port - Port number of the AEM instance
cq_user - User ID to connect to the AEM Instance	
cq_password - Password of the AEM User ID
tag_namespace - Tags namespace to check and find all tags under it 
```


## Other key configuration entries
The current configuration has the right entries for these properties. These properties might need to be changed if needed. Following are such properties:
```
tags_output_file - The output CSV file path that stores all the tags extracted
```

## Input files
```
tags_template_file - The CSV template with headers for writing the output tags to
```

## Output files
```
tags_output_file - Default configured to output/tags_output.csv contains all the tags extracted under the given namespace
```

## How to run
### After the correct configurations are done and input files placed in the folder, run the script tags-x.py by executing the below command under this script folder
```
python tags-x.py 
```


---
> Environment Tested on:  AEM6.2, Python 2.7.15 

