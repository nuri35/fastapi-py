from base64 import b64encode
import bcrypt



def get_password_hash(password):
    salt = bcrypt.gensalt(rounds=12, prefix=b'2b')
    key = b64encode(bcrypt.hashpw(str(password).encode("ascii"), salt))
    return key