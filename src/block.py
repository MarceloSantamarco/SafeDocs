from datetime import datetime
from Crypto.Hash import SHA256
class Block:

    def __init__(self, data, previous_id, difficulty, previous_hash):
        self.id = previous_id+1
        self.difficulty = difficulty
        self.nonce = 1
        self.created_at = str(datetime.now(tz=None))
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.create_hash()

    def create_hash(self):
        h = SHA256.new()
        h = SHA256.new(bytes(str(self.__dict__), 'utf-8'))
        return h.hexdigest()