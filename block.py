from datetime import datetime
import hashlib
import application_helper as helper

class Block:
    
    def __init__(self, data, previous_hash, previous_id, difficulty):
        self.id = previous_id+1
        self.difficulty = difficulty
        self.nonce = 1
        self.created_at = str(datetime.now(tz=None))
        self.data = data
        self.hash = self.create_hash()

    def create_hash(self):
        sha = hashlib.sha256()
        sha.update(helper.serialize(self).encode('utf-8'))
        return sha.hexdigest()