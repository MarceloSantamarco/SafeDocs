from flask import Flask, request, render_template
import json

from src.blockchain import Blockchain
from src.address import Address
from src.application_helper import serialize

app = Flask(__name__)

bc = Blockchain()
adresses = {}

@app.route("/", methods=["GET"])
def home():
    return serialize(bc)

@app.route("/address/new", methods=["GET"])
def new_address():
    ad = Address()

    adresses[ad.__dict__["address"]] = []

    return serialize(ad)
    
@app.route("/address/find", methods=["GET"])
def find_user_documents():
    try:
        docs = adresses[request.form.get("address")]
    except KeyError:
        docs = {'error': 'Address is not found'}
    return json.dumps(docs) if len(docs) > 0 else {}

@app.route("/block/available", methods=["GET"])
def available():
    dic = bc.__dict__
    if dic["opened_block"] == None:
        return {}    
    else:
        return serialize(dic["opened_block"])

@app.route("/blockchain/mine", methods=["GET"])
def mine():
    try:
        bc.mine_block()
    except ConnectionError:
        return {"error": "Block is not available"}
    else:
        return serialize(bc.chain[-1])

@app.route("/document/new", methods=["POST"])
def new_document():
    try:
        adresses[request.form.get("address")]
    except KeyError:
        return {"error": "Address not found"}
    try:
        if bc.new_document(request.files["document"]):
            adresses[request.form.get("address")].append(bc.pool[-1])
            return serialize(bc.pool[-1])
        else:
            return {"error": "Invalid Signature"}
    except ValueError:
        return {"error": "The document is not available"}

@app.route("/document/verify", methods=["GET"])
def verify_document():
    doc = request.files["document"]
    for i in bc.chain:
        for j in i['data']:
            if j['doc'] == str(doc.read(), 'utf-8', 'replace'):
                return serialize(j)
    return {'status': 404}

@app.route("/document/digital_certificate", methods=["GET"])
def issue_certificate():
    # doc_id = request.params.get("document")
    # address = request.form.get("address")
    # for i in adresses[address]:
    #     if i['id'] == doc_id:
    return render_template('certificate.html')