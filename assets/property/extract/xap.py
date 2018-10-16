import csv, os, re, urllib, json, urllib2, base64
from aemigrate_commons import *
from aemigrate_utilities import *
import logging, logging.handlers
import time, copy

s_time = get_timestamp()

#Load config
cfg = load_config()

# Initialize loggers
trace = get_logger(cfg['trace_log'])
error = get_logger(cfg['error_log'])
status = get_output_handler(cfg['status_log'])

path_list = []

def loadPathList(path):
    global path_list
    trace.info("Loading configured path list for processing")
    with open(path,'rb') as pFile:
        #For each row in csv
        path_list = pFile.read().splitlines()
    trace.info("Done... paths loaded: \n"+ "\n".join(path_list) +"\n\n")
    trace.info("Count: "+ str(len(path_list)) + " paths loaded for processing")

def isInList(path):
    global path_list
    if path in path_list:
        return True
    for row in path_list:
        if  row in path:
            return True
    return False

def getMetaVal(asset, key):
    path = key.split('/')
    p_obj = asset
    try:
        for k in path:
            p_obj = p_obj[k]
    except:
        return None
    return p_obj

def logStatus(msg):
    status.info(msg)
    print msg


trace.info("Initializing...")

rec_count = 0

loadPathList(cfg['path_list'])


#Form URL to fetch metadata for the given path
url = cfg['cq_protocal']+'://'+cfg['cq_user']+':'+cfg['cq_password']+'@'+cfg['cq_host']+':'+cfg['cq_port']+'/bin/querybuilder.json?type=dam:Asset&path='+cfg['base_path']+'&p.limit=-1&p.hits=selective&p.properties='+' '.join(cfg['extract_properties'])+'&p.nodedepth=-1'

#Fetch metadata
trace.info('Fetching metadata of all assets for processing')
response = urllib.urlopen(url).read()

#Parse metadata to identify all assets
trace.info('Parsing asset metadata...')
data = json.loads(response)

try:

    # Write headers of extracted properties to properties_before_migration CSV
    with open(cfg['properties_output'],'ab') as propsCSV:
        wr = csv.writer(propsCSV, dialect='excel')
        row = []
        for key in cfg['extract_properties']:
            row.append(key)
        wr.writerow(row)

        for asset in data[cfg['asset_json_node']]:

            a_path = asset[cfg['path_json_node']]

            if isInList(a_path):
                try:
                    trace.info('Checking asset : '+a_path)
                    rec_count += 1

                    trace.info('Writing properties to CSV for : '+a_path)

                    row = []
                    for key in cfg['extract_properties']:
                        r_value = getMetaVal(asset,key)
                        trace.info('Writing properties to CSV for : r_value '+r_value)
                        if bool == type(r_value): 
                            r_value = "Booelan - "+ str(r_value)
                        row.append(encode_list(r_value))
                    wr.writerow(row)
                except  Exception, e:
                    #error.error('Error in writing properties to CSV')
                    error.error('Exception occured...'+a_path)
                    trace.error('Error in writing properties to CSV')
                
except  Exception, e:
    error.error('Error in writing properties to CSV')
    #error.error('Exception occured...'+a_path)
    trace.error('Error in writing properties to CSV')

#Print final status
logStatus("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
logStatus("Migration Run Started at   : "+s_time)
logStatus("Migration Run Completed at : "+get_timestamp()+"\n")
logStatus("Status")
logStatus("======")
logStatus("Total Assets : "+str(rec_count))
logStatus("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")

