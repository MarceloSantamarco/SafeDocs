import json
import sqlite3
import fitz

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

def create_connection():
    return sqlite3.connect('test_database') 

def read_fitz(certificate):
    with fitz.open(stream=certificate.read(), filetype="pdf") as doc:
        text = []
        for page in doc:
            text.append(page.get_text().split(':'))
        return text[0][2].replace('\n', '').replace(' ', '').replace('Carimbodetempo', '')