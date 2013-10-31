import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'): 
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)
        
def members_to_list(members):
    result = []
    for item in members:
        result.append(member_to_dict(item, key = None))
    return result; 

def member_to_dict(member, key):
    D = dict([(p, getattr(member, p)) for p in member.properties()])
    if key is None:
        D['id'] = member.key().id()
    else:
        D['id'] = key.id()
    
    del D['pin']
    return D

def object_to_json(object):
    return json.dumps(object, cls=JSONEncoder)

def success_result(main, result, extra_value):
    dic_for_json = {'code':200};
    
    if extra_value is not None:
        for key, value in extra_value.items():
            dic_for_json[key] = value
            
    dic_for_json['result'] = result
    main.response.write(object_to_json(dic_for_json))  

def fail_result(main, code, message):
    main.response.write(object_to_json({'code':code, 'message':message}))