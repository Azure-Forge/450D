import os
import shutil
from dotenv import load_dotenv
from getpass import getpass
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import numpy as np

# Load password from .env
load_dotenv()
password = os.getenv("MY_SECRET_PASSWORD")
if password is None:
    password = getpass("Enter encryption password: ")

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
BIN_DIR = os.path.join(BASE_DIR, 'bin')

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def encrypt_file(npy_path, enc_path, password):
    # Generate a random salt and nonce
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    # Read npy file as bytes
    with open(npy_path, 'rb') as f:
        data = f.read()
    ct = aesgcm.encrypt(nonce, data, None)
    # Write salt + nonce + ciphertext
    with open(enc_path, 'wb') as f:
        f.write(salt + nonce + ct)

def decrypt_file(enc_path, password):
    with open(enc_path, 'rb') as f:
        blob = f.read()
    salt = blob[:16]
    nonce = blob[16:28]
    ct = blob[28:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    data = aesgcm.decrypt(nonce, ct, None)
    return data

def encrypt_all_npy():
    for fname in os.listdir(DATA_DIR):
        if fname.endswith('.npy'):
            npy_path = os.path.join(DATA_DIR, fname)
            enc_path = os.path.join(DATA_DIR, fname.replace('.npy', '.enc'))
            print(f"Encrypting {fname} -> {os.path.basename(enc_path)}")
            encrypt_file(npy_path, enc_path, password)
            # Move original npy to bin
            shutil.move(npy_path, os.path.join(BIN_DIR, fname))

def load_decrypted_npy(enc_path, password):
    data = decrypt_file(enc_path, password)
    # Load numpy array from decrypted bytes
    from io import BytesIO
    return np.load(BytesIO(data))

if __name__ == "__main__":
    encrypt_all_npy()
    print("All .npy files encrypted and moved to bin/.")

