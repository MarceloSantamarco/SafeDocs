from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import json

from src.blockchain import Blockchain
from src.user import User
from src.session import Session
from src.application_helper import serialize

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

bc = Blockchain()
adresses = {}

@app.route("/", methods=["GET"])
def home():
    return serialize(bc)

@app.route("/address/new", methods=["POST"])
@cross_origin()

def new_address():

    try:
        user = User(request.form.get("name"), request.form.get("email"), request.form.get("password"))

        adresses[user.__dict__["address"]] = []

        return {
            user: user.__dict__
        }
    except ValueError:
        return {
            'error': 'email already exists'
        }

@app.route("/session/new", methods=["POST"])
@cross_origin()

def new_session():

    try:
        session  = Session(request.form.get("email"), request.form.get("password"))
        adresses[session.__dict__["address"]] = []
        return {
            'session': session.__dict__
        }
    except ValueError:
        return {
            'error': 'invalid email or password' 
        }
    
@app.route("/address/find", methods=["GET"])
@cross_origin()

def find_user_documents():
    try:
        docs = adresses[request.args.get("address")]
    except KeyError:
        docs = {'error': 'Address is not found'}
    return json.dumps(docs) if len(docs) > 0 else {}

@app.route("/block/available", methods=["GET"])
@cross_origin()

def available():
    dic = bc.__dict__
    if dic["opened_block"] == None:
        return {}    
    else:
        return serialize(dic["opened_block"])

@app.route("/blockchain/mine", methods=["GET"])
@cross_origin()

def mine():
    try:
        bc.mine_block()
    except ConnectionError:
        return {"error": "Block is not available"}
    else:
        return serialize(bc.chain[-1])

@app.route("/document/new", methods=["POST"])
@cross_origin()

def new_document():
    try:
        adresses[request.args.get("address")]
    except KeyError:
        return {"error": "Address not found"}
    try:
        if bc.new_document(request.files["document"]):
            adresses[request.args.get("address")].append(bc.pool[-1])
            return serialize(bc.pool[-1])
        else:
            return {"error": "Invalid Signature"}
    except ValueError:
        return {"error": "The document is not available"}

@app.route("/document/verify", methods=["GET"])
@cross_origin()

def verify_document():
    doc = request.files["document"]
    for i in bc.chain:
        for j in i['data']:
            if j['doc'] == str(doc.read(), 'utf-8', 'replace'):
                return serialize(j)
    return {'status': 404}

@app.route("/document/digital_certificate", methods=["GET"])
@cross_origin()

def issue_certificate():
    doc = request.files["document"]
    address = request.args.get("address")
    for i in bc.chain:
        for j in i['data']:
            if j['doc'] == str(doc.read(), 'utf-8', 'replace'):
                i=50
                x=j['signature']
                while i <= len(j['signature']):
                    x = f"{x[:i]}\n{x[i:]}"
                    i+=50
                return render_template('certificate.html', doc=j, address=address, signature=x)
    return {'status': 404}