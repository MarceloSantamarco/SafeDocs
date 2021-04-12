import json

def serialize(obj):
    obj = obj.__dict__
    for key in obj:
        try:
            obj[key] = obj[key].__dict__
        except:
            pass
    print(obj)
    return json.dumps(obj)