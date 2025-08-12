import os
import shutil
import subprocess
import math
import secrets
import numpy as np


def generate_450d_array():
    """Generate 450 secure random floats in [0,1) from 64-bit unsigned integers."""
    ints = np.frombuffer(secrets.token_bytes(450 * 8), dtype=np.uint64)
    return ints / np.float64(2**64)


def create_weight_matrix(num_dims, num_pixels):
    """Create a small-weight matrix of shape (num_dims, num_pixels) with CSPRNG floats."""
    ints = np.frombuffer(secrets.token_bytes(num_dims * num_pixels * 8), dtype=np.uint64)
    floats = ints / np.float64(2**64)
    return floats.reshape(num_dims, num_pixels) * 0.0005


def stack_dimensions(arr, weights):
    """Multiply 1D array by weights matrix (dot product)."""
    return arr @ weights


def pixel_values_to_rgb_image(r_vals, g_vals, b_vals):
    """
    Convert three 1D arrays into padded, normalized RGB images.
    Returns raw padded values, normalized values, and image size.
    """
    size = int(math.ceil(math.sqrt(len(r_vals))))
    padded_length = size * size

    def normalize_and_pad(channel_vals):
        padded = np.zeros(padded_length)
        padded[:len(channel_vals)] = channel_vals
        norm = (padded - padded.min()) / (padded.max() - padded.min() + 1e-8)
        return padded, norm

    r_raw, r_norm = normalize_and_pad(r_vals)
    g_raw, g_norm = normalize_and_pad(g_vals)
    b_raw, b_norm = normalize_and_pad(b_vals)

    # Reshape channels to 2D images
    r_raw = r_raw.reshape((size, size))
    g_raw = g_raw.reshape((size, size))
    b_raw = b_raw.reshape((size, size))

    r_norm = r_norm.reshape((size, size))
    g_norm = g_norm.reshape((size, size))
    b_norm = b_norm.reshape((size, size))

    rgb_raw = np.stack([r_raw, g_raw, b_raw], axis=2).astype(np.float32)
    rgb_norm = np.stack([r_norm, g_norm, b_norm], axis=2).astype(np.float32)

    return rgb_raw, rgb_norm, size


def archive_existing_encrypted_files():
    """Move existing .enc files from data directory to a numbered archive folder in secret directory."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data')
    secret_dir = os.path.join(base_dir, 'generation')

    # Find next archive index
    existing = [d for d in os.listdir(secret_dir) if d.isdigit()]
    next_idx = max(map(int, existing), default=0) + 1

    archive_dir = os.path.join(secret_dir, str(next_idx))
    os.makedirs(archive_dir, exist_ok=True)

    # Move .enc files to archive folder
    for fname in os.listdir(data_dir):
        if fname.endswith('.enc'):
            shutil.move(os.path.join(data_dir, fname), os.path.join(archive_dir, fname))


if __name__ == "__main__":
    # Archive existing encrypted files if any
    archive_existing_encrypted_files()

    # Generate base array
    arr = generate_450d_array()
    num_pixels = 22 * 22

    # Generate weight matrices for each RGB channel
    weights_r = create_weight_matrix(len(arr), num_pixels)
    weights_g = create_weight_matrix(len(arr), num_pixels)
    weights_b = create_weight_matrix(len(arr), num_pixels)

    # Apply weights to base array to get pixel values
    r_vals = stack_dimensions(arr, weights_r)
    g_vals = stack_dimensions(arr, weights_g)
    b_vals = stack_dimensions(arr, weights_b)

    # Convert pixel values to raw and normalized RGB images
    rgb_raw, rgb_norm, size = pixel_values_to_rgb_image(r_vals, g_vals, b_vals)

    # Save arrays to data folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data')
    np.save(os.path.join(data_dir, "arr.npy"), arr)
    np.save(os.path.join(data_dir, "weights_r.npy"), weights_r)
    np.save(os.path.join(data_dir, "weights_g.npy"), weights_g)
    np.save(os.path.join(data_dir, "weights_b.npy"), weights_b)
    np.save(os.path.join(data_dir, "rgb_raw.npy"), rgb_raw)
    np.save(os.path.join(data_dir, "rgb_norm.npy"), rgb_norm)

    print(f"Data generated and saved. Image size: {size}x{size}")

    # Run encryption script
    encrypt_script = os.path.join(os.path.dirname(__file__), "transform_npy.py")
    subprocess.run(["python3", encrypt_script], check=True)
