import csv, os, re, urllib, json
from aemigrate_commons import *
from aemigrate_utilities import *
import logging, logging.handlers


#Parse run configuration
cfg = load_config()

# Initialize loggers
trace = get_logger(cfg['trace_log'])
error = get_logger(cfg['error_log'])
status = get_logger(cfg['status_log'])

# Initialize output file handler (uses log library)
m_handle = get_output_handler(cfg['metadata_file'])

rec_count = 0
skip_count = 0
err_count = 0


trace.info("Initializing...")

#Form URL to fetch all the tags
url = cfg['cq_protocal']+'://'+cfg['cq_user']+':'+cfg['cq_password']+'@'+cfg['cq_host']+':'+cfg['cq_port']+'/bin/querybuilder.json?type=cq:Tag&path=/etc/tags/'+cfg['tag_namespace']+'&p.limit=-1&p.hits=selective&p.properties=jcr:path jcr:title jcr:description&orderby=path'

#Fetch tags
trace.info('Fetching all tags for migration')
response = urllib.urlopen(url).read()

#Write meatadata to file
trace.info('Writing metadata to '+cfg['metadata_file'])
m_handle.info(response)

all_tags = json.loads(response)
trace.info('Fetched all tags from source')

# Copy template to output folder
shutil.copy(cfg['tags_template_file'],cfg['tags_output_file'])

with open(cfg['tags_output_file'],'ab') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')

    for tag_data in all_tags['hits']:
		rec_count += 1
		try:
			encode(tag_data)
			#Get name & parent of the tag
			path = tag_data.pop('jcr:path')
			name = path[path.rindex('/')+1:]
			parent = path[:path.rindex('/')][10:]
			title = tag_data.get('jcr:title','')
			desc = tag_data.get('jcr:description')

			row = [path,title,desc]
			wr.writerow(row)
			trace.error('Processed tag...'+str(path))
		except:
			trace.error('Error processing tag...')
			error.error('Error processing tag...')
			err_count += 1
			

trace.info('Tag extraction complete...')

#Print final status
status.info("....................................................................")
status.info("Processing Completed")
status.info("Total Tags : "+str(rec_count))
status.info("Successful : "+str(rec_count - (skip_count + err_count)))
status.info("Skipped : "+str(skip_count))
status.info("Failed : "+str(err_count))
if(err_count or skip_count):
    status.info("Check the file at "+cfg['error_log']+" for error and skipped details")

relax()

