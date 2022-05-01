from charm.toolbox.pairinggroup import PairingGroup, G1, ZR

group = PairingGroup('BN254')

def serialize(A):
    return list( group.serialize(A))

def hash_id(id):
    return group.hash(id, G1)

def deserialize(obj):
    return group.deserialize(bytes(obj))

def get_x():
    return group.random(ZR)
