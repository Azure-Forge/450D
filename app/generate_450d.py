import numpy as np
import math

def generate_450d_array():
    return np.random.rand(450)

def create_weight_matrix(num_dims, num_pixels):
    return np.random.rand(num_dims, num_pixels) * 0.0005  # smaller scale to reduce noise

def stack_dimensions(arr, weights):
    return arr @ weights

def pixel_values_to_rgb_image(r_vals, g_vals, b_vals):
    size = int(math.ceil(math.sqrt(len(r_vals))))
    padded_length = size * size
    
    def normalize_and_pad(channel_vals):
        padded = np.zeros(padded_length)
        padded[:len(channel_vals)] = channel_vals
        norm = (padded - padded.min()) / (padded.max() - padded.min() + 1e-8)
        return padded, norm  # return raw and normalized for saving and debugging

    r_raw, r_norm = normalize_and_pad(r_vals)
    g_raw, g_norm = normalize_and_pad(g_vals)
    b_raw, b_norm = normalize_and_pad(b_vals)

    # Reshape to 2D before stacking
    r_raw = r_raw.reshape((size, size))
    g_raw = g_raw.reshape((size, size))
    b_raw = b_raw.reshape((size, size))

    r_norm = r_norm.reshape((size, size))
    g_norm = g_norm.reshape((size, size))
    b_norm = b_norm.reshape((size, size))

    rgb_raw = np.stack([r_raw, g_raw, b_raw], axis=2).astype(np.float32)
    rgb_norm = np.stack([r_norm, g_norm, b_norm], axis=2).astype(np.float32)

    return rgb_raw, rgb_norm, size


if __name__ == "__main__":
    arr = generate_450d_array()
    num_pixels = 22 * 22
    
    weights_r = create_weight_matrix(len(arr), num_pixels)
    weights_g = create_weight_matrix(len(arr), num_pixels)
    weights_b = create_weight_matrix(len(arr), num_pixels)
    
    r_vals = stack_dimensions(arr, weights_r)
    g_vals = stack_dimensions(arr, weights_g)
    b_vals = stack_dimensions(arr, weights_b)
    
    rgb_raw, rgb_norm, size = pixel_values_to_rgb_image(r_vals, g_vals, b_vals)
    
    # Save everything
    np.save("../data/arr.npy", arr)
    np.save("../data/weights_r.npy", weights_r)
    np.save("../data/weights_g.npy", weights_g)
    np.save("../data/weights_b.npy", weights_b)
    np.save("../data/rgb_raw.npy", rgb_raw)
    np.save("../data/rgb_norm.npy", rgb_norm)
    
    print(f"Data generated and saved. Image size: {size}x{size}")