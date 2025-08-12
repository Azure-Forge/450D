

import os
from transform_npy import load_decrypted_npy, DATA_DIR, get_password

def load_array(name, data_dir=None, password=None):
    if data_dir is None:
        data_dir = DATA_DIR
    enc_path = os.path.join(data_dir, f"{name}.enc")
    if password is None:
        password = get_password()
    return load_decrypted_npy(enc_path, password)

def list_available_arrays(data_dir=None):
    if data_dir is None:
        data_dir = DATA_DIR
    return [f[:-4] for f in os.listdir(data_dir) if f.endswith('.enc')]

if __name__ == "__main__":
    arrays = list_available_arrays()
    print("Available arrays:", arrays)
    arr = load_array('arr')
    print("arr shape:", arr.shape)
