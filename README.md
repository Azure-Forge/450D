# 450D Secure Secret Encryption

## Overview
This project provides a secure workflow for generating, encrypting, and using secrets as high-dimensional arrays, with all sensitive data encrypted at rest. The encryption uses AES-GCM with a password from your `.env` file, and all decryption is performed in memory only when needed.

## How It Works
1. **Secret Generation**
    - Run `python app/generate_450d.py` to generate a new set of secrets.
    - This script creates a random 450-dimensional array and associated weight matrices, then saves them as `.npy` files in the `data/` directory.
    - Any existing encrypted secrets (`.enc` files) are archived in `secret/1`, `secret/2`, etc., before new data is generated.
    - After generation, the script automatically encrypts the new `.npy` files using AES-GCM and your password, then moves the originals to `bin/`.

2. **Encryption/Decryption Workflow**
    - All secrets are stored as encrypted `.enc` files in `data/`.
    - When you need to use a secret, it is decrypted in memory only (never written to disk in plaintext).
    - The password is loaded from `.env` (variable: `MY_SECRET_PASSWORD`). If not found, you will be prompted once per session.

3. **Testing the System**
    - Edit `app/index.py` and change the `plaintext` variable to any message you want to encrypt.
    - Run `python app/index.py` to:
        - Load and decrypt the required arrays in memory.
        - Encode and encrypt your message into RGB values (ciphertext arrays).
        - Decrypt the RGB values and recover the original message.
        - Print both the ciphertext arrays and the recovered message.

## File Structure
- `app/generate_450d.py`: Generates new secrets and encrypts them.
- `app/transform_npy.py`: Handles encryption/decryption of `.npy` files.
- `app/loader.py`: Loads and decrypts arrays in memory as needed.
- `app/crypto.py`: Provides message encoding, encryption, and decryption logic.
- `app/index.py`: Example script to test the full workflow.
- `data/`: Stores encrypted secrets (`.enc` files).
- `bin/`: Stores original `.npy` files after encryption (for erasure simulation).
- `secret/`: Archives previous encrypted secrets.
- `.env`: Stores your password (variable: `MY_SECRET_PASSWORD`).

## Security Notes
- All sensitive data is encrypted at rest using AES-GCM.
- The password is never hardcoded; it is loaded from `.env` or prompted securely.
- Decryption is always performed in memory, and plaintext arrays are never written to disk.
- Previous secrets are archived for backup and audit purposes.

## Quick Start
1. Set your password in `.env`:
   ```
   MY_SECRET_PASSWORD=your_strong_password
   ```
2. Generate new secrets:
   ```
   python app/generate_450d.py
   ```
3. Edit `app/index.py` and set your message in the `plaintext` variable.
4. Run the test:
   ```
   python app/index.py
   ```

You will see the ciphertext arrays and the recovered message printed to the console.

---

For more details, see the code and comments in each script.
