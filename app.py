from flask import Flask, request

from src.blockchain import Blockchain
from src.address import Address
from src.application_helper import serialize

app = Flask(__name__)
bc = Blockchain()

@app.route("/", methods=['GET'])
def home():
    return serialize(bc)

@app.route("/address/new", methods=['GET'])
def new_address():
    ad = Address()
    return serialize(ad)
    

@app.route("/block/available", methods=['GET'])
def available():
    return {} if bc.__dict__['opened_block'] == None else serialize(bc.__dict__['opened_block'])

@app.route("/blockchain/mine", methods=['GET'])
def mine():
    try:
        bc.mine_block()
    except ConnectionError:
        return {'error': 'Block is not available'}
    else:
        return bc.chain[-1]

@app.route("/document/new", methods=['POST'])
def new_document():
    try:
        if bc.new_document(request.files["document"]):
            return serialize(bc.pool[-1])
        else:
            return {'error': 'Invalid Signature'}
    except ValueError:
        return {'error': 'The document is not available'}