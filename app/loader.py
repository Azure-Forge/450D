import numpy as np
import os

def load_all_data(data_dir=None):
    if data_dir is None:
        # Default: data folder next to the project root
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

    arr = np.load(os.path.join(data_dir, 'arr.npy'))
    rgb_norm = np.load(os.path.join(data_dir, 'rgb_norm.npy'))
    rgb_raw = np.load(os.path.join(data_dir, 'rgb_raw.npy'))
    weights_b = np.load(os.path.join(data_dir, 'weights_b.npy'))
    weights_g = np.load(os.path.join(data_dir, 'weights_g.npy'))
    weights_r = np.load(os.path.join(data_dir, 'weights_r.npy'))

    return {
        'arr': arr,
        'rgb_norm': rgb_norm,
        'rgb_raw': rgb_raw,
        'weights_b': weights_b,
        'weights_g': weights_g,
        'weights_r': weights_r,
    }

if __name__ == "__main__":
    data = load_all_data()
    print("Loaded data keys:", list(data.keys()))
    print("arr shape:", data['arr'].shape)
    print("rgb_norm shape:", data['rgb_norm'].shape)
