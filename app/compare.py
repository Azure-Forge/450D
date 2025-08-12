
import os
import numpy as np
from dotenv import load_dotenv
from getpass import getpass
from transform_npy import load_decrypted_npy, BIN_DIR, DATA_DIR

def main():
	load_dotenv()
	password = os.getenv("MY_SECRET_PASSWORD")
	if password is None:
		password = getpass("Enter encryption password: ")

	all_match = True
	for fname in os.listdir(DATA_DIR):
		if fname.endswith('.enc'):
			base = fname.replace('.enc', '')
			enc_path = os.path.join(DATA_DIR, fname)
			npy_path = os.path.join(BIN_DIR, base + '.npy')
			if not os.path.exists(npy_path):
				print(f"Missing original: {npy_path}")
				all_match = False
				continue
			arr_dec = load_decrypted_npy(enc_path, password)
			arr_orig = np.load(npy_path)
			if np.array_equal(arr_dec, arr_orig):
				print(f"MATCH: {base}")
			else:
				print(f"MISMATCH: {base}")
				all_match = False
	if all_match:
		print("All arrays match!")
	else:
		print("Some arrays do not match.")

if __name__ == "__main__":
	main()


