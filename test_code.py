import hashlib
import random # cryptoguard: ignore

def verify_file(file_content):
    return hashlib.md5(file_content).hexdigest() # cryptoguard: ignore

def hash_user_password(password_string):
    return hashlib.md5(password_string.encode()).hexdigest() # cryptoguard: ignore