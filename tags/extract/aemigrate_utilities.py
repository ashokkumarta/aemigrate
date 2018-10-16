import re, urllib, json, httplib, sys
from aemigrate_commons import *

# Have all utility functions here, & include this file in user_migrate.py

def checkmailsyntax(email):
    return (not email) or (re.match(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\b", email.strip()))

def validatephone(phone):
   return (not phone) or (re.match(r"\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}", phone))

def validVal(val, list):
    return (not val) or (val.strip() in list)

def unique(val, cont, key):
    coll = cont.get(key)
    if (not coll):
        coll = []
    if (val.strip() not in coll):
        coll.append(val)
        cont[key] = coll
        return True
    return False

def mappedVal(val, list):
    if val in list:
        return list[val]
    return val


def get_sql(data, map, sqlTpl):
    keys = []
    vals = []
    for col in data:
        keys.append(map.get(col))
        vals.append(data.get(col))
    r_keys = sqlTpl.replace('$KEYS$',", ".join(keys))
    return r_keys.replace('$VALUES$','"'+'", "'.join(vals)+'"')


def postJson(server, path, content, hdr, t_log):
    try: 
        conn = httplib.HTTPConnection(server)
        t_log.info('Connection established with the server')
        conn.request('POST', path, json.dumps(content, encoding='latin1'), hdr)
        t_log.info('Sponsor invite request sent')
        r_res = conn.getresponse()
        p_res = processResponse(r_res, t_log)
        t_log.info('Sponsor invite response processed')
        return p_res
    except:
        t_log.error('Unexpected error in sponsor invite request processing : '+str(sys.exc_info()[0]))
        return {"h_status":500, "r_status":500, "r_desc":"ERROR" }
        

def processResponse(r_res, t_log):
    p_res = {}
    t_log.info('Sponsor invite response : '+str(r_res))
    status = r_res.status
    t_log.info('Sponsor invite response status: '+str(status))
    data = r_res.read()
    t_log.info('Sponsor invite response data: '+str(data))
    j_res = json.loads(data)
    p_res["h_status"] = status
    p_res["r_status"] = j_res['responseCode']
    p_res["r_desc"] = j_res['responseDescription']
    return p_res

def mapSpl(val, spec, data):
    if not val:
        return val
    type = spec["type"]
    if "A" == type:
        for k, v in spec.iteritems():
            if k != "type":
                data[k] = v
    return val

def get_msql(val, sqlTpl):
    return sqlTpl.replace('$USER_ID$','"'+val+'"')

def encode(obj):
    for k, v in obj.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        obj[k] = v
