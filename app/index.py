from crypto import encode_message, encrypt, decrypt, decode_message, load_crypto_arrays

# Load all required arrays (decrypted in memory only when needed)
arr, weights_r, weights_g, weights_b, rgb_norm = load_crypto_arrays()

plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
message_vector = encode_message(plaintext)

r_vals, g_vals, b_vals = encrypt(message_vector, arr, weights_r, weights_g, weights_b, rgb_norm)

print("Ciphertext arrays:")
print("r_vals:", r_vals)
print("g_vals:", g_vals)
print("b_vals:", b_vals)

recovered_vector = decrypt(r_vals, g_vals, b_vals, weights_r, weights_g, weights_b, arr, rgb_norm)
recovered_message = decode_message(recovered_vector)

print("Recovered message:", recovered_message)
