from base64 import b64encode
import bcrypt



def get_password_hash(password):
    key = bcrypt.hashpw(password = password.encode("utf-8"),  salt=bcrypt.gensalt())
    return key.decode('utf-8')


def check_password(hashed, password):
    # "Unicode-objects must be encoded before checking against bcrypt hash"
    check_data = bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8"))
    return check_data

