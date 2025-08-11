from loader import load_all_data
from crypto import encode_message, encrypt, decrypt, decode_message
import numpy as np

data = load_all_data()

arr = data['arr']
weights_r = data['weights_r']
weights_g = data['weights_g']
weights_b = data['weights_b']
rgb_norm = data['rgb_norm']

plaintext = "Hello, world!"
message_vector = encode_message(plaintext)

r_vals, g_vals, b_vals = encrypt(message_vector, arr, weights_r, weights_g, weights_b, rgb_norm)

print("Ciphertext arrays:")
print("r_vals:", r_vals)
print("g_vals:", g_vals)
print("b_vals:", b_vals)

recovered_vector = decrypt(r_vals, g_vals, b_vals, weights_r, weights_g, weights_b, arr, rgb_norm)
recovered_message = decode_message(recovered_vector)

print("Recovered message:", recovered_message)
