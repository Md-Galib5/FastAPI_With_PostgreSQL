from pwdlib import PasswordHash

Password_hash = PasswordHash.recommended()

def hash_password(password : str):
    return Password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return Password_hash.verify(plain_password,hashed_password)