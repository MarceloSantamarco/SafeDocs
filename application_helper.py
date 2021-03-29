import json

def serialize(obj):
    return json.dumps(obj.__dict__)