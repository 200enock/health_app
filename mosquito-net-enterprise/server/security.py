import hashlib, os
def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16)
    pwd = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + pwd
def verify_password(stored, password):
    salt = stored[:16]
    return stored == hash_password(password, salt)
