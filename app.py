from blockchain import Blockchain
from address import Address

ad = Address()
print(ad.__dict__)

bc = Blockchain()
print(bc.__dict__)

bc.new_document('./test.txt')
bc.new_document('./test2.txt')

bc.mine_block()

print(bc.__dict__['genesis'].__dict__)