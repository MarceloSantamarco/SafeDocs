from block import Block
import json

class Blockchain:

    def __init__(self):
        self.chain = []
        self.pool = []
        self.opened_block = None
        self.genesis = self.create_genesis()

    def create_genesis(self):
        docs = {
            'doc1': 'aaa',
            'doc2': 'bbb',
            'doc3': 'ccc'
        }
        genesis = Block(docs, '0000', 0, 5)
        self.opened_block = genesis
        return genesis

    def new_block(self):
        self.opened_block = Block(self.pool, self.chain[-1]['hash'], self.chain[-1]['id'], self.chain[-1]['difficulty']+1)

    def mine_block(self):
        block = self.opened_block.__dict__
        difficulty = block['difficulty']
        while 1:
            hasher = self.opened_block.create_hash()
            hash_difficulty_slice = list(set([char for char in hasher][0:difficulty]))
            if hash_difficulty_slice[0] == '0' and len(hash_difficulty_slice) == 1:
                block['hash'] = hasher
                self.chain.append(block)
                print(f"Bloco #{block['id']}, com dificuldade #{block['difficulty']} foi minerado com nonce #{block['nonce']} e hash #{block['hash']}")
                break
            else:
                block['nonce']+=1
