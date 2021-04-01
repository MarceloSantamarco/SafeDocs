from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, RIPEMD160

class Address:

    def __init__(self):
        self.address = self.generate_address()

    def generate_address(self):
        p_key = self.generate_keys()
        h = SHA256.new()
        h.update(p_key.export_key(format='PEM', passphrase=None, pkcs=1, protection=None, randfunc=None))
        r = RIPEMD160.new()
        r.update(bytes(h.hexdigest(), 'utf-8'))
        return r.hexdigest()

    def generate_keys(self):
        password = Random.get_random_bytes(12)
        self.generate_private_key(password)
        
        return RSA.import_key(open('private_key.pem', 'rb').read(), passphrase=password).publickey()

    def generate_private_key(self, password):
        key = RSA.generate(2048)
        private_key = key.export_key(format='PEM', passphrase=password, pkcs=1)
        file_out = open("private_key.pem", "wb")
        file_out.write(private_key)
        file_out.close()
        f = open('password.txt', 'wb')
        f.write(password)
        f.close()
