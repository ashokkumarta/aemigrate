# aemigrate - Create Asset Folder Taxonomy 

Creates folder taxonomy for the asset based on the given input

## Configuration to change
```
cq_host - Host name of the AEM instance to connect to 
cq_port - Port number of the AEM instance
cq_user - User ID to connect to the AEM Instance	
cq_password - Password of the AEM User ID
base_path - Base DAM path under which the given taxonomy gets created
input_file - Path to the input csv file that contains the taxonomy structure to create
```

## Other key configuration entries
```
None
```

## Input files
```
input_file - The csv file that contains the taxonomy structure to create
```

## Output files
```
None
```

## How to run
After the correct configurations are done and input files placed in the folder, run the script cat.py by executing the below command under this script folder
```
python cat.py 
```

---
> Environment Tested on:  AEM6.2, Python 2.7.15 
