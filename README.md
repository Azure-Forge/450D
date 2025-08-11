Usage

    Generate the 450D array
    Run generate_450d.py first to create the initial RGB array.

    Encrypt a message
    After the array is generated, you can set any message in index.py.
    The system encrypts the message into the RGB values within the 450D array as ciphertext.

    Recover the message
    The encrypted RGB data can then be decoded back to recover the original message.

How It Works


We use a multidimensional array (typically 3D), where each element corresponds to a pixel’s color, represented by three values: Red, Green, and Blue (RGB).
RGB Value Generation

For each pixel position, the system generates or assigns RGB values—integers in the range 0 to 255—that define the pixel's color.
Populating the Array

These RGB values are stored in the array at the corresponding positions, creating a full representation of the image or dataset.
Result

The resulting array encodes color information as a digital image or dataset, which can be processed, displayed, or transformed.
