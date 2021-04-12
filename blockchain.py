from block import Block
from document import Document
import json
class Blockchain:

    def __init__(self):
        self.chain = []
        self.pool = []
        self.opened_block = None
        self.genesis = None

    def create_genesis(self):
        genesis = Block(self.pool, '0', 0, 5)
        self.opened_block = genesis
        self.genesis = genesis
        return genesis

    def new_block(self):
        self.opened_block = Block(self.pool, self.chain[-1]['hash'], self.chain[-1]['id'], self.chain[-1]['difficulty']+1)

    def mine_block(self):
        if self.opened_block is None:
            raise Exception("Block is not available")
        block = self.opened_block.__dict__
        difficulty = block['difficulty']
        while 1:
            hasher = self.opened_block.create_hash()
            hash_difficulty_slice = list(set([char for char in hasher][0:difficulty]))
            if hash_difficulty_slice[0] == '0' and len(hash_difficulty_slice) == 1:
                block['hash'] = hasher
                self.chain.append(block)
                print(f"Bloco #{block['id']}, com dificuldade #{block['difficulty']} foi minerado com nonce #{block['nonce']} e hash #{block['hash']}")
                self.opened_block = None
                break
            else:
                block['nonce']+=1
    
    def new_document(self, doc):
        if doc is None:
            raise ValueError
        document = Document(doc)
        if document.check_signature():
            document.create_id(self.__dict__)
            self.pool.append(document.__dict__)
            if len(self.pool) > 1:
                self.create_genesis() if len(self.chain) == 0 else self.new_block()
            return True
        else:
            return False