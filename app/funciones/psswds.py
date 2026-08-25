from argon2 import PasswordHasher

ph = PasswordHasher()

def hasher (str: str):
    password = str
    res = ph.hash(password)
    return res

def comparar_hash (str: str, hash: str):
    password = str
    try:
        res = ph.verify(hash, password)
        return res
    except:
        return False
