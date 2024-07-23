import hashlib


# hashing

def hashing_password(password):
    pass_encode=password.encode()
    hashed_password=hashlib.sha256(pass_encode).hexdigest()
    return hashed_password
