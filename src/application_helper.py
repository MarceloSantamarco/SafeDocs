import json

def serialize(obj):
    try:
        obj = obj.__dict__
    except AttributeError:
         pass
    for key in obj:
        if type(obj[key]) == bytes:
            obj[key] = str(obj[key], 'utf-8', 'replace')
        else:
            try:
                obj[key] = obj[key].__dict__
            except:
                pass
    return json.dumps(obj)
    