import csv, os, re, urllib, json, urllib2, base64
from aemigrate_commons import *
from aemigrate_utilities import *
import logging, logging.handlers
import time, copy

s_time = get_timestamp()

assets_to_update = {}
types_of_props = {}

#Load config
cfg = load_config()

# Initialize loggers
trace = get_logger(cfg['trace_log'])
error = get_logger(cfg['error_log'])
status = get_output_handler(cfg['status_log'])

# Initialize output file handler (uses log library)
s_handle = get_output_handler(cfg['successful_assets'])
f_handle = get_output_handler(cfg['failed_assets'])
n_handle = get_output_handler(cfg['skipped_assets'])

def loadAssetsToUpdate():
    global assets_to_update
    global types_of_props
    trace.info("Loading assets to update from CSV file ")
    with open(cfg['assets_to_update'],'r') as aFile:
        # Process header
        header = next(aFile).strip()
        props_to_update = header.split(",")
        types = next(aFile).strip()
        types_list = types.split(",")
        for i, p in enumerate(props_to_update):
            types_of_props[p] = types_list[i]


        trace.info("Properties to update : " + str(props_to_update))
        trace.info("Types of properties : " + str(types_of_props))

        if "jcr:path" != props_to_update[0]:
            error.error('Error... Invalid input file')
            error.error('The first column must be jcr:path property')
            error.error('Terminating the program')
            sys.exit() 
        
        #For each record in csv
        for r in aFile:
            trace.info("Loading rec..."+str(r))
            vals = r.strip().split(",")
            assets_to_update[vals[0]] = {}
            for i in range(1,len(vals)):
                assets_to_update[vals[0]][props_to_update[i]] = vals[i]

    trace.info("Loaded the assets to be updated...")
    trace.info("Count: "+ str(len(assets_to_update)))

def isInList(path):
    global assets_to_update
    if path in assets_to_update:
        return True
    return False


def post_multipart(host, selector, headers, fields):
    content_type, body = encode_multipart_formdata(fields)
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    for (key, value) in headers.iteritems():
        h.putheader(key, value)
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read(), errcode

def encode_multipart_formdata(fields):
    LIMIT = '----------lImIt_of_THE_fIle_eW_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields.iteritems():
        L.append('--' + LIMIT)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    L.append('--' + LIMIT + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % LIMIT
    return content_type, body

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
err_count = 0
nota_count = 0

loadAssetsToUpdate()


#Form URL to fetch metadata for the given path
url = cfg['cq_protocal']+'://'+cfg['cq_user']+':'+cfg['cq_password']+'@'+cfg['cq_host']+':'+cfg['cq_port']+'/bin/querybuilder.json?type=dam:Asset&path='+cfg['base_path']+'&p.limit=-1&p.hits=selective&p.properties='+' '.join(cfg['extract_properties'])+'&p.nodedepth=-1'

#Fetch metadata
trace.info('Fetching metadata of assets for processing')
response = urllib.urlopen(url).read()

#Parse metadata to identify all assets
trace.info('Parsing asset metadata...')
data = json.loads(response)

# Prepare URL opener for update
trace.info('Initializing url connection parameters to update assets')

u_base64string = base64.encodestring('%s:%s' % (cfg['cq_user'], cfg['cq_password'])).replace('\n', '')
u_base_url = cfg['cq_host']+':'+cfg['cq_port']

header = {}
header['Authorization'] = 'Basic %s' % u_base64string

try:

    # Open properties_before_migration CSV for logging
    with open(cfg['properties_output'],'ab') as propsCSV:
        wr = csv.writer(propsCSV, dialect='excel')
        row = []
        # Write headers of extracted properties to properties_before_migration CSV
        for key in cfg['extract_properties']:
            row.append(key)
        wr.writerow(row)

        for asset in data[cfg['asset_json_node']]:

            a_path = asset[cfg['path_json_node']]

            if isInList(a_path):

                trace.info('Checking asset : '+a_path)
                rec_count += 1
                try:

                    trace.info('Writing properties before migration to output CSV file')

                    row = []
                    for key in cfg['extract_properties']:
                        r_value = getMetaVal(asset,key)
                        if bool == type(r_value): 
                            trace.info("appending type : "+str(type(r_value))) 
                            r_value = "Booelan - "+ str(r_value)
                        row.append(encode_list(r_value))
                    wr.writerow(row)

                    # Send size update request with new value
                    # Log reponse status

                except  Exception, e:
                    #error.error('Error in writing properties to CSV')
                    error.error('Exception occured...'+a_path)
                    trace.error('Error in writing properties before migration to CSV')

                try:
                    update_properties = {}
                    trace.info('Initializing for asset update')
                    # Get correct size value
                    rec = assets_to_update[a_path]

                    if (rec):
                    

                        trace.info('Constituting the properties to update')

                        #Get asset path
                        api_a_path = a_path[12:]

                        update_properties['_charset_'] = 'utf-8'
                        update_properties['dam:bulkUpdate'] = 'true'
                        update_properties['mode'] = 'hard'
                        for p in cfg['update_properties']:
                            trace.info('Checking property : '+str(p))
                            if p in rec and (rec[p] or cfg['update_blank']):
                                update_properties['.' + api_a_path + '/' + p] = rec[p]
                                if(types_of_props[p]):                      
                                    update_properties['.' + api_a_path + '/' + p + '@TypeHint'] = types_of_props[p]

                        trace.info('Updating asset with : '+json.dumps(update_properties))
                        
                        response, status_code = post_multipart(u_base_url, '/content/dam.html', header, update_properties)
                        
                        trace.debug('Request sent...')

                        time.sleep(cfg["time_wait_secs"])
                        trace.debug('Response received... Status : '+ str(status_code))

                        # check response status
                        if (status_code == 200):
                            s_handle.info(a_path)
                            trace.info('Update completed for : ' + a_path)
                        else:
                            error.error('Update failed for : ' + a_path)
                            error.error('Error Code : ' + str(status_code))
                            error.error('Error Response : '+str(response))
                            trace.error('Update failed for : ' + a_path)
                            err_count += 1
                            f_handle.info(a_path)
                            
                    else:
                        trace.error('Update skipped for : ' + a_path)
                        nota_count += 1
                        n_handle.info(a_path)

                except Exception, e:
                    error.error('Update failed for : ' + a_path)
                    error.error('Exception occured...'+str(e))
                    trace.error('Update failed for : ' + a_path)
                    err_count += 1
                    f_handle.info(a_path)

                
except  Exception, e:
    error.error('Error... Unexpected exception')
    error.error('Exception details...'+str(e))
    error.error('Error... Unexpected exception')

time.sleep(cfg["time_wait_secs"])

#Print final status
logStatus("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
logStatus("Migration Run Started at   : "+s_time)
logStatus("Migration Run Completed at : "+get_timestamp()+"\n")
logStatus("Status")
logStatus("======")
logStatus("Total Assets : "+str(rec_count))
logStatus("Successful : "+str(rec_count - (nota_count + err_count)))
logStatus("Skipped (size not set) : "+str(nota_count))
logStatus("Failed : "+str(err_count))
if(err_count or nota_count):
    logStatus("Check the file at "+cfg['error_log']+" for error and skipped details")

logStatus("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")

