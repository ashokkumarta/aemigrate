import csv
import os
import re
import urllib, json
from aemigrate_commons import *
from aemigrate_utilities import *
import logging, logging.handlers


#Load config
cfg = load_config()

# Initialize loggers
trace = get_logger(cfg['trace_log'])
error = get_logger(cfg['error_log'])
status = get_logger(cfg['status_log'])

# Initialize output file handler (uses log library)
a_handle = get_output_handler(cfg['assets_file'])
m_handle = get_output_handler(cfg['metadata_file'])

rec_count = 0
skip_count = 0
err_count = 0


trace.info("Initializing...")


#Form URL to fetch metadata for the given path
url = cfg['cq_protocal']+'://'+cfg['cq_user']+':'+cfg['cq_password']+'@'+cfg['cq_host']+':'+cfg['cq_port']+'/bin/querybuilder.json?type=dam:Asset&path='+cfg['assets_in_path']+'&p.limit=-1&p.nodedepth=-1'

#Fetch metadata
trace.info('Fetching metadata for all assets')
response = urllib.urlopen(url).read()

#Write meatadata to file
trace.info('Writing metadata to '+cfg['metadata_file'])
m_handle.info(response)

#Parse metadata to identify all assets
trace.info('Parsing metadata to identify all asset paths')
data = json.loads(response)

trace.info('Writing asset paths to '+cfg['assets_file'])


for asset in data[cfg['asset_json_node']]:
	rec_count += 1
	try:
		#Write fully qualified paths for each asset to file for download
		a_handle.info(asset[cfg['path_json_node']])
		trace.info('Found asset at '+asset[cfg['path_json_node']])
	except:
		trace.error('Error finding asset...')
		error.error('Error finding asset...')
		err_count += 1


print 'Details fetched for all assets at: '+ cfg['assets_in_path']

#Print final status
status.info("....................................................................")
status.info("Processing Completed")
status.info("Total Assets : "+str(rec_count))
status.info("Successful : "+str(rec_count - (skip_count + err_count)))
status.info("Skipped : "+str(skip_count))
status.info("Failed : "+str(err_count))
if(err_count or skip_count):
    status.info("Check the file at "+cfg['error_log']+" for error and skipped details")

relax()

