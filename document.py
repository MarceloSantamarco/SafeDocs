import application_helper as helper
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

class Document: 

    def __init__(self):
        self.id = None
        self.doc_bins = ''
        self.signature = self.generate_signature()

    def generate_signature(self):
        data = helper.serialize(self)
        modulus_length = 256*4
        privatekey = RSA.generate(modulus_length, data)
        publickey = privatekey.publickey()
        return privatekey, publickey