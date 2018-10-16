
import urllib, json,  csv, shutil
from aemigrate_commons import *
from aemigrate_utilities import *


def create(ele):
	path = cname(curr_base)
	name = cname(ele)
	req_url = aem_url + path+'/'
	post_fields[':name'] = name
	post_fields['./jcr:content/jcr:title'] = ele
	urllib.urlopen(req_url,urllib.urlencode(post_fields))

#Load config
cfg = load_config()

# Initialize loggers
trace = get_logger(cfg['trace_log'])

aem_url = cfg['cq_protocal']+'://'+cfg['cq_user']+':'+cfg['cq_password']+'@'+cfg['cq_host']+':'+cfg['cq_port']+cfg['base_path']

post_fields = { './jcr:primaryType': 'sling:OrderedFolder', './jcr:content/jcr:primaryType':'nt:unstructured', '_charset_':'utf-8' }

curr_base = []

with open(cfg['input_file'], 'rb') as csvfile:
    all_folders = csv.reader(csvfile, delimiter=',', quotechar='|')
    for folder in all_folders:
        level = baseInd(curr_base,folder)
        curr_base = curr_base[:level]
        for ele in folder[level:]:
            if(len(ele) > 0):
                create(ele)
                curr_base.append(ele)
                trace.info('Created Folder: ' + '/'.join(curr_base))
relax()
