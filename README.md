# 450D Secure Secret Demo

## How it works
- Generate a new secret set: `python app/generate_450d.py`
    - Archives old encrypted secrets in `secret/1`, `secret/2`, ... 
    - Generates new random arrays and encrypts them with your password from `.env`.
- Edit `app/index.py` and set any message you want to encrypt in the `plaintext` variable.
- Run the demo: `python app/index.py`
    - Shows the RGB ciphertext arrays and the decrypted message.

## Example
```
$ python app/generate_450d.py
Data generated and saved. Image size: 22x22
All .npy files encrypted and moved to bin/.

$ python app/index.py
Ciphertext arrays:
r_vals: [ ... ]
g_vals: [ ... ]
b_vals: [ ... ]
Recovered message: Hello, world!
```

Set your password in `.env` as `MY_SECRET_PASSWORD=your_strong_password`.

For more details, see the code and comments in each script.
