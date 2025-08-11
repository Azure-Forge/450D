import numpy as np

def encode_message(message, length=450):
    ascii_vals = [ord(c) for c in message]
    if len(ascii_vals) < length:
        ascii_vals += [0] * (length - len(ascii_vals))  # pad zeros
    else:
        ascii_vals = ascii_vals[:length]  # truncate
    return np.array(ascii_vals, dtype=np.float32)

def decode_message(vector):
    chars = [chr(int(round(x))) for x in vector if 0 <= int(round(x)) < 128]
    return "".join(chars)

def generate_noise_mask(rgb_norm, length, amplitude=0.05):
    noise_source = rgb_norm.flatten()
    noise = noise_source[:length] * amplitude
    return noise

def encrypt(message_vector, arr, weights_r, weights_g, weights_b, rgb_norm, noise_amplitude=0.05):
    combined = message_vector + arr
    noise = generate_noise_mask(rgb_norm, len(combined), noise_amplitude)
    combined_noisy = combined + noise

    r_vals = combined_noisy @ weights_r
    g_vals = combined_noisy @ weights_g
    b_vals = combined_noisy @ weights_b

    return r_vals, g_vals, b_vals

def decrypt(r_vals, g_vals, b_vals, weights_r, weights_g, weights_b, arr, rgb_norm, noise_amplitude=0.05):
    weights_r_inv = np.linalg.pinv(weights_r)
    weights_g_inv = np.linalg.pinv(weights_g)
    weights_b_inv = np.linalg.pinv(weights_b)

    combined_r = r_vals @ weights_r_inv
    combined_g = g_vals @ weights_g_inv
    combined_b = b_vals @ weights_b_inv

    combined_noisy = (combined_r + combined_g + combined_b) / 3

    noise = generate_noise_mask(rgb_norm, len(combined_noisy), noise_amplitude)
    combined = combined_noisy - noise

    message_vector = combined - arr
    return message_vector
