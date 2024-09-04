# Scramblify
![Screenshot 2024-09-04 202430](https://github.com/user-attachments/assets/7c3045af-ff1c-443e-832e-09b1c563df5a)

## Overview

Scramblify is an advanced image encryption tool that allows you to securely encrypt and decrypt images using pixel manipulation combined with AES encryption. It offers a simple drag-and-drop interface for easy image selection, making it accessible even for users without a technical background.

## Features

- **Encryption and Decryption**: Encrypt images using a 6-character key and decrypt them with the same key.
- **Pixel Manipulation**: Scramble the pixels of your image for an additional layer of security before applying AES encryption.
- **User-Friendly Interface**: Simple drag-and-drop feature, along with options to browse, encrypt, and decrypt images.
- **Cross-Platform**: Compatible with both Windows and Linux systems.

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python packages: `numpy`, `Pillow`, `tkinterdnd2`, `pycryptodome`

### Steps to Run on Windows

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Jibinjoseph22/Scramblify.git
    cd Scramblify
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    ```bash
    python scramblify.py
    ```

### Steps to Run on Linux

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Jibinjoseph22/Scramblify.git
    cd Scramblify
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Tkinter** (if not already installed):
    - For Ubuntu/Debian:
        ```bash
        sudo apt-get install python3-tk
        ```
    - For Fedora:
        ```bash
        sudo dnf install python3-tkinter
        ```

4. **Run the Application**:
    ```bash
    python3 scramblify.py
    ```

## Usage

1. Launch the application.
2. Drag and drop an image into the application or use the "Browse Image" button to select a file.
3. Enter a 6-character key in the provided field.
4. Click "Encrypt Image" to encrypt the image or "Decrypt Image" to decrypt it.
5. Save the resulting file in your desired location.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.


