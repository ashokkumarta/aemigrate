import csv, os, re, urllib, json, urllib2, base64
from aemigrate_commons import *
from aemigrate_utilities import *
import logging, logging.handlers
import time


#Load config
cfg = load_config()

# Initialize loggers
trace = get_logger(cfg['trace_log'])
error = get_logger(cfg['error_log'])
status = get_logger(cfg['status_log'])

# Initialize output file handler (uses log library)
s_handle = get_output_handler(cfg['successful_tags'])
f_handle = get_output_handler(cfg['failed_tags'])


legacy_tags = {}
new_tags = {}

def addLegacyTag(t_data):
    global legacy_tags
    try:
        legacy_tags[t_data[0]] = { 'title':t_data[1], "desc":t_data[2] }
    except:
        trace.error('Invalid legacy tag : '+ str(t_data))
        error.error('Invalid legacy tag : '+ str(t_data))
    
def getLegacyDetails(t_data):
    global legacy_tags
    legacy_keys = legacy_tags.keys()
    if t_data in legacy_keys:
        return legacy_tags[t_data]["title"], legacy_tags[t_data]["desc"]
    return "", ""

def getParentTagId(n_tag):
    try:
        p_id = n_tag[:n_tag.rindex('/')]
        p_fetch = n_tag[:n_tag[:n_tag.rindex('/')].rindex('/')]
        #Make URL connection
        #Form URL to fetch parent tags Json
        url = cfg['cq_protocal']+'://'+cfg['cq_user']+':'+cfg['cq_password']+'@'+cfg['cq_host']+':'+cfg['cq_port']+p_fetch+'.tags.json'
        #Fetch metadata
        trace.info('Fetching parent tags Json for : '+p_fetch)
        response = urllib.urlopen(url).read()
        #Parse response and store it in parent tags
        trace.info('Parsing response and storing it in parent tags...')
        p_tags_data = json.loads(response)

        return matchParentTagId(p_id, p_tags_data)
    except:
        trace.error('Error fetching parent tag id for : '+ str(n_tag))
        error.error('Error fetching parent tag id for : '+ str(n_tag))
    return None

def matchParentTagId(id, tson_data):

    for t in tson_data['tags']:
        trace.info('matchParentTagId : path : '+t['path'])
        if t['path'] == id:
            trace.info('Matched')
            trace.info('Returning parent tag ID : '+str(t['tagID']))
            return t['tagID']
    return None

def getTagName(n_tag):
    if n_tag:
        return n_tag[n_tag.rindex('/')+1:]
    return None

def err(msg):
    trace.error(msg)
    error.error(msg)
    raise ValueError(msg)

def warn(msg):
    trace.warn(msg)
    error.warn(msg)

trace.info("Initializing...")



rec_count = 0
skip_count = 0
err_count = 0

# Read legacy tags from csv and store in json
for x_file in cfg['legacy_tags_extract']:
    trace.info("Loading legacy tags from : "+x_file)
    with open(x_file,'rb') as l_tagsCSV:
        reader = csv.reader(l_tagsCSV)
        # Skip hearder row
        next(reader, None)
        for r in reader:
            addLegacyTag(r)
    trace.info("Completed loading legacy tags from : "+x_file)
    trace.info("Legacy tags accumulated : "+str(len(legacy_tags.keys())))
        
trace.info("Starting processing of new tags from "+cfg['new_tags_mapping'])
with open(cfg['new_tags_mapping'],'rb') as n_tagsCSV:
    reader = csv.reader(n_tagsCSV)
    # Skip hearder row
    next(reader, None)
    trace.info("Loading mapping of new tag entries")
    for r in reader:
        rec_count = rec_count + 1
        try: 
            new_tags[r[0]] = r[1]
        except:
            trace.error('Error in preprocessing tag : '+str(r))
            error.error('Error in preprocessing tag : '+str(r))
            err_count = err_count + 1

new_ordered_tags = new_tags.keys()
new_ordered_tags.sort()

# Prepare URL opener for new tags creation
trace.info('Initializing url connection to create tags')
u_opener = urllib2.build_opener(urllib2.HTTPHandler)
u_base64string = base64.encodestring('%s:%s' % (cfg['cq_user'], cfg['cq_password'])).replace('\n', '')
u_base_url = cfg['cq_protocal']+'://'+cfg['cq_host']+':'+cfg['cq_port']+'/bin/tagcommand'

trace.info('Url connection initialized')


for t in new_ordered_tags:
    trace.info("Processing tag "+str(t))
    error.info("Starting Tag : "+str(t))
    try: 
        pt_id = getParentTagId(t)
        if not pt_id:
            warn('Invalid parent tag id : '+str(pt_id))
            err('One or more parent path tags missing')
            
        name = getTagName(t)
        if not name:
            err('Invalid tag name : '+str(name))

        trace.debug('Fetching legacy details for : ' + t)
        trace.debug('Fetching legacy details from : ' + new_tags[t])
        title, desc = getLegacyDetails(new_tags[t])

        if not title:
            warn("Title not set in the corresponding legacy tag. Using name as title")
            title = name
        if not desc:
            warn("Description not set in the corresponding legacy tag. Leaving it blank")

        tag_data = {'cmd':'createTag'}
        tag_data['parentTagID']=pt_id
        tag_data['tag']=name
        tag_data['jcr:title']=title
        tag_data['jcr:description']=desc

        trace.info("Tag data ready!!!")
        # fetch parent tagId
        # Create new tag

        trace.info("Inititating connection...")
        #Set URL & Data
        request = urllib2.Request(u_base_url, data=urllib.urlencode(tag_data))
        trace.debug('URL Created : ' + u_base_url)
        trace.debug('Sending Data : ' + urllib.urlencode(tag_data))

        #Set headers and method
        request.add_header('Authorization', 'Basic %s' % u_base64string) 
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        request.get_method = lambda: 'POST'
        trace.debug('Headers set...')

        #Execute metadata update
        response = u_opener.open(request)

        trace.debug('Request sent...')

        #Print the response
        trace.debug('Response received...')
        if cfg['log_response']:
            trace.info(response.read())
        trace.info('Successfully created tag : '+t)
        error.info("Done")
        s_handle.info(t)

    except urllib2.HTTPError as err:
        trace.error('HTTPError creating tag : '+t)
        error.error('HTTPError creating tag : '+t)
        error.error('HTTPError : '+ str(err))
        f_handle.info(t)
        err_count = err_count + 1
        
    except:
        trace.error('Error creating tag : '+t)
        error.error('Error creating tag : '+t)
        error.error('Unexpected error : '+ str(sys.exc_info()[0]))
        f_handle.info(t)
        err_count = err_count + 1

    time.sleep(cfg["time_wait_secs"])


trace.info('Tag creation complete...')

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

                        