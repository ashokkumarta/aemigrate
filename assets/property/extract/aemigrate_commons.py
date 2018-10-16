import os, json, shutil, collections
import logging, logging.handlers
from datetime import datetime

def load_config():
    'Loads the config file and returns json object'
    config_file = 'cfg/run_config.json'
    print 'Reading config path'
    try: 
           config_file = os.environ['RUN_CONFIG']
    except KeyError, e:
        print 'Config path not defined. Using default path'
    
    print 'Loading configuration file '+config_file
    config=open(config_file).read()
    print 'configuration parameters:\n'+config
    return json.loads(config)

def get_logger(track):
    'Returns a logger for the track'
    _format_ = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    _handler_ = logging.handlers.RotatingFileHandler(track);
    _handler_.setFormatter(_format_)

    _logger_ = logging.getLogger(track)
    _logger_.addHandler(_handler_)
    _logger_.addHandler(logging.StreamHandler())
    _logger_.setLevel(logging.DEBUG)

    return _logger_

def get_output_handler(handle):
    'Returns a logger for the track'

    _handler_ = logging.handlers.RotatingFileHandler(handle);
    _logger_ = logging.getLogger(handle)
    _logger_.addHandler(_handler_)
    _logger_.setLevel(logging.INFO)
    return _logger_
    
def get_timestamp():
    return datetime.now().strftime('%d %b %Y, %H:%M:%S')

def encode(obj):
    for k, v in obj.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        obj[k] = v

def encode_list(obj):
    if isinstance(obj, list):
        e_obj = []
        for v in obj:
            if isinstance(v, unicode):
                v = v.encode('utf8')
            e_obj.append(v)
        return "\n".join(e_obj)
    elif isinstance(obj, str):
        return obj.encode('utf8')
    else:
        return obj

def get_element(asset,key):
    val = asset
    for index in key:
        if index in val:
            val = val.get(index)
        else:
            return ""
    return val

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def get_asset(value):
    #Get path & name of the asset
    name = value[value.rindex('/')+1:]
    parent = value[:value.rindex('/')]
    return parent,name

def relax():
    'Done... Check logs for more details'
    print '\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n'
