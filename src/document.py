from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
from datetime import datetime
class Document:

    def __init__(self, doc, address):
        self.id = None
        self.doc = doc.read()
        self.doc_name = doc.filename
        self.doc_extension = doc.filename.split('.')[1]
        self.signature = self.generate_signature(address)
        self.timestamp = str(datetime.now(tz=None))

    def generate_signature(self, address):
        key = RSA.import_key(open(f'./{address}/private_key.pem', 'rb').read(), passphrase=open(f'./{address}/password.txt', 'rb').read())
        h = SHA256.new(base64.b64encode(self.doc))
        return base64.b64encode(pkcs1_15.new(key).sign(h))

    def check_signature(self, address):
        key = RSA.import_key(open(f'./{address}/private_key.pem', 'rb').read(), passphrase=open(f'./{address}/password.txt', 'rb').read())
        h = SHA256.new(base64.b64encode(self.doc))
        try:
            pkcs1_15.new(key).verify(h, base64.b64decode(self.signature))
            print("Signature verifyed!")
            return True
        except (ValueError, TypeError):
            print("Invalid signature!")
            return False

    def create_id(self, blockchain):
        docs_previous_block = [] if blockchain['chain'] == [] else blockchain['chain'][-1]['data']
        docs_current_pool = blockchain['pool']
        if docs_current_pool == []: 
            if docs_previous_block == []:
                self.id = 1
            else:
                self.id = docs_previous_block[-1]['id']+1
        else:
           self.id = docs_current_pool[-1]['id']+1
        return True