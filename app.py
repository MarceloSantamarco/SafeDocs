from blockchain import Blockchain

bc = Blockchain()

print(bc.__dict__['genesis'].__dict__)

bc.mine_block()
print()

print(bc.__dict__['chain'])

bc.new_block()

print(bc.__dict__['opened_block'].__dict__)

bc.mine_block()
print()

print(bc.__dict__['chain'])