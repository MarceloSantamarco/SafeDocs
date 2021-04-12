from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import base64
class Document:

    def __init__(self, doc):
        self.id = None
        self.doc = open(doc, 'rb').read()
        self.signature = self.generate_signature()

    def generate_signature(self):
        key = RSA.import_key(open('private_key.pem', 'rb').read(), passphrase=open('password.txt', 'rb').read())
        h = SHA256.new(base64.b64encode(self.doc))
        return pkcs1_15.new(key).sign(h)

    def check_signature(self):
        key = RSA.import_key(open('private_key.pem', 'rb').read(), passphrase=open('password.txt', 'rb').read())
        h = SHA256.new(base64.b64encode(self.doc))
        try:
            pkcs1_15.new(key).verify(h, self.signature)
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