from blockchain import Blockchain
from address import Address

ad = Address()
print(ad.__dict__)

bc = Blockchain()

bc.new_document('doc1')
bc.new_document('doc2')
bc.new_document('doc3')
bc.new_document('doc4')

bc.mine_block()

print(bc.__dict__['genesis'].__dict__)