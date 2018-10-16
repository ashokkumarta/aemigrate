# aemigrate - AEM migration utilities 
> Ashokkumar T A | 15-Oct-2018

A set of AEM migration utilities. The scripts covers the utilities for asset files, asset properties, asset folders & tags. These scripts are developed in Python & shell scripts & are tested on RHEL5 environment. All the testing was done on AEM 6.2, but should work on other versions of AEM as well. Though its tested on Linux environment, most of these scripts can be run on Windows as well and includes windows command line scripts where helpful.  

## Dependencies
```
Python 2.7 - The scripts were developed on Python 2.7
```

## General Usage

All the scripts follow a standard structure. Where there is a deviation from this, the documentation of that script details it. 

### Standard folder structure
```
Script folder - contains the script, dependent libraries, command line & shell script utilities and other folders
cfg - configurations folder. This folder has one key configuration file - run_config.json which holds the configuration for the run
in - inputs folder. This folder contains the input files reqiuired for the run
logs - log files folder. This folder has all the logs generated from the run
out - outputs folder. This folder contains all the output files created by the run 
```

### Commands
Under each scripts, a set of command line & shell scripts are present which can be leverages for the run
```
do.sh - Shell script that executes the run
do.cmd - Windows command script that executes the run
cl.sh - Shell script that clears up the logs and output from the previous run
cl.cmd - Windows command script that clears up the logs and output from the previous run
``` 

### Includes
+ Utitities for handling asset binaries (uploading, downloading)
+ Utilities for handling asset properties (extracting, updating, fetching the asset list)
+ Utility for creating asset folder taxonomy
+ Utilities for managing tags (creating, extracting)


### Reservation
> These scripts are created for specific use cases. Make sure its tested for your scenario before applying it for production purpose

---
> Environment Tested on:  AEM6.2, Python2.7.15, RHEL5 





