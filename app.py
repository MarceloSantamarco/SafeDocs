from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import json

from src.blockchain import Blockchain
from src.user import User
from src.session import Session
from src.application_helper import serialize, read_fitz

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
            'session': {
                'name': user.name,
                'email': user.email,
                'address': user.address
            }
        }, 200
    except ValueError:
        return {
            'error': 'E-mail já cadastrado!'
        }, 400

@app.route("/session/new", methods=["POST"])
@cross_origin()

def new_session():

    try:
        session  = Session(request.form.get("email"), request.form.get("password"))
        try:
            adresses[session.__dict__["address"]]
        except KeyError:
            adresses[session.__dict__["address"]] = []
        else:
            pass
        return {
            'session': session.__dict__
        }
    except ValueError:
        return {
            'error': 'E-mail ou senha incorretos!' 
        }, 404
    
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
        return {"error": "Block is not available"}, 400
    else:
        return serialize(bc.chain[-1])

@app.route("/document/new", methods=["POST"])
@cross_origin()

def new_document():
    try:
        adresses[request.form.get("address")]
    except KeyError:
        return {"error": "Address not found"}, 400
    try:
        if bc.new_document(request.files["document"], request.form.get("address")):
            adresses[request.form.get("address")].append(bc.pool[-1])
            serialize(bc.pool[-1])
            mine()
            return adresses[request.form.get("address")][-1]
        else:
            return {"error": "Invalid Signature"}, 400
    except ValueError:
        return {"error": "The document is not available"}, 400

@app.route("/document/verify", methods=["POST"])
@cross_origin()

def verify_document():
    doc = request.files["document"]
    certificate = request.files["certificate"]
    reading = str(doc.read(), 'utf-8', 'replace')
    signature = read_fitz(certificate)
    for i in bc.chain:
        for j in i['data']:
            if j['doc'] == reading and j['signature'] == signature:
                return serialize(j)
    return {
        'status': 400,
        'message': 'Invalid document!'
    }, 400

@app.route("/document/digital_certificate", methods=["POST"])
@cross_origin()

def issue_certificate():
    reading = request.form.get("doc")
    address = request.form.get("address")
    for i in bc.chain:
        for j in i['data']:
            if j['doc'] == reading:
                i=50
                x=j['signature']
                while i <= len(j['signature']):
                    x = f"{x[:i]}\n{x[i:]}"
                    i+=50
                return render_template('certificate.html', doc=j, address=address, signature=x)
    return {
        'status': 400,
        'message': 'Invalid document!'
    }, 400