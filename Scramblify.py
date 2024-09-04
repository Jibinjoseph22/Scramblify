import numpy as np
from PIL import Image, ImageTk, UnidentifiedImageError
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from Crypto.Cipher import AES
import os
import hashlib
import struct


class AdvancedImageEncryptionTool:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Advanced Image Encryption Tool with Drag and Drop")
        self.root.geometry("650x500") 
        self.root.configure(bg='lightgray')

        self.image_path = ""
        self.original_shape = None
        self.is_encrypted = False

        self.setup_ui()

    def setup_ui(self):
        
        self.description_label = tk.Label(self.root, text=(
            "Welcome to the Advanced Image Encryption Tool! This application allows you "
            "to encrypt and decrypt images using a key. You can drag and drop an image or "
            "use the 'Browse Image' button to select an image file. For encryption, specify a "
            "6-character key and save the encrypted file. For decryption, load the encrypted file, "
            "enter the key, and save the decrypted image. Use the buttons below to perform these operations."),
            bg='lightgray', fg='black', wraplength=600, justify='left', font=('Arial', 12))
        self.description_label.pack(pady=10)

        
        self.image_label = tk.Label(self.root, text="Drag and drop an image here or use Browse", width=50, height=10, relief="groove", bg='white', fg='black')
        self.image_label.pack(pady=20)

        
        self.browse_button = tk.Button(self.root, text="Browse Image", command=self.browse_image, bg='lightblue', fg='black')
        self.browse_button.pack(pady=10)

     
        self.encrypt_button = tk.Button(self.root, text="Encrypt Image", command=self.encrypt_image, state=tk.DISABLED, bg='darkgreen', fg='white')
        self.encrypt_button.pack(pady=10)

        
        self.decrypt_button = tk.Button(self.root, text="Decrypt Image", command=self.decrypt_image, state=tk.DISABLED, bg='darkred', fg='white')
        self.decrypt_button.pack(pady=10)

        
        self.key_label = tk.Label(self.root, text="Enter Key (6 characters):", state=tk.DISABLED, bg='lightgray', fg='black')
        self.key_label.pack(pady=10)

        
        self.key_entry = tk.Entry(self.root, show="*", state=tk.DISABLED)
        self.key_entry.pack(pady=5)

        
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.enc")])
        if self.image_path:
            self.process_file()

    def on_drop(self, event):
        self.image_path = event.data.strip('{}')
        if os.path.isfile(self.image_path):
            self.process_file()
        else:
            messagebox.showerror("Error", "No valid file detected.")

    def process_file(self):
        try:
            if self.image_path.endswith('.enc'):
                self.is_encrypted = True
                self.display_image(None)  # Clear image 
                self.key_label.config(state=tk.NORMAL)
                self.key_entry.config(state=tk.NORMAL)
                self.decrypt_button.config(state=tk.NORMAL)
                self.encrypt_button.config(state=tk.DISABLED)
            else:
                self.is_encrypted = False
                self.display_image(self.image_path)
                self.key_label.config(state=tk.NORMAL)
                self.key_entry.config(state=tk.NORMAL)
                self.encrypt_button.config(state=tk.NORMAL)
                self.decrypt_button.config(state=tk.DISABLED)

        except UnidentifiedImageError:
            messagebox.showerror("Error", "The dropped file is not a valid image or encrypted file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")

    def display_image(self, img_path):
        if img_path:
            try:
                image = Image.open(img_path)
                image.thumbnail((250, 250))
                img_tk = ImageTk.PhotoImage(image)
                self.image_label.config(image=img_tk, text="")
                self.image_label.image = img_tk
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display image: {e}")
        else:
            self.image_label.config(image=None, text="Encrypted file loaded. Ready to decrypt.")
            self.image_label.image = None

    def validate_key(self):
        key = self.key_entry.get()
        if len(key) != 6:
            messagebox.showerror("Error", "Key must be exactly 6 characters long.")
            return None
        return key

    def extend_key(self, key):
        return hashlib.sha256(key.encode()).digest()[:16]

    def generate_iv(self):
        return os.urandom(16)

    def scramble_pixels(self, array, key):
        flat_array = array.flatten()
        np.random.seed(int(hashlib.sha256(key.encode()).hexdigest(), 16) % (2**32))
        indices = np.random.permutation(flat_array.size)
        scrambled_array = flat_array[indices]
        return scrambled_array, indices

    def unscramble_pixels(self, scrambled_array, indices, shape):
        unscrambled_array = np.zeros_like(scrambled_array)
        unscrambled_array[indices] = scrambled_array
        return unscrambled_array.reshape(shape)

    def aes_encrypt(self, data, key):
        key_bytes = self.extend_key(key)
        iv = self.generate_iv()
        cipher = AES.new(key_bytes, AES.MODE_CFB, iv)
        encrypted_data = iv + cipher.encrypt(data)
        return encrypted_data

    def aes_decrypt(self, encrypted_data, key):
        key_bytes = self.extend_key(key)
        iv = encrypted_data[:16]
        cipher = AES.new(key_bytes, AES.MODE_CFB, iv)
        decrypted_data = cipher.decrypt(encrypted_data[16:])
        return decrypted_data

    def encrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image loaded!")
            return
        key = self.validate_key()
        if key is None:
            return

        try:
            image = Image.open(self.image_path)
            image_array = np.array(image)
            self.original_shape = image_array.shape
            scrambled_array, indices = self.scramble_pixels(image_array, key)
            scrambled_bytes = scrambled_array.tobytes()
            encrypted_bytes = self.aes_encrypt(scrambled_bytes, key)

            encrypted_path = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted Files", "*.enc")])
            if not encrypted_path:
                return

            with open(encrypted_path, 'wb') as f:
                shape_bytes = struct.pack('III', *self.original_shape)
                f.write(shape_bytes)
                f.write(encrypted_bytes)
                f.write(np.array(indices, dtype=np.int32).tobytes())
            messagebox.showinfo("Success", f"Image encrypted and saved as '{os.path.basename(encrypted_path)}'")
            self.reset_state()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to encrypt the image: {e}")

    def decrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image loaded!")
            return

        key = self.validate_key()
        if key is None:
            return

        try:
            with open(self.image_path, 'rb') as f:
                shape_bytes = f.read(12)
                if len(shape_bytes) < 12:
                    raise ValueError("Invalid file format: missing shape data.")
                self.original_shape = struct.unpack('III', shape_bytes)

                encrypted_bytes = f.read()
                indices_size = np.prod(self.original_shape)
                indices_bytes_size = indices_size * 4
                encrypted_data = encrypted_bytes[:-indices_bytes_size]
                indices = np.frombuffer(encrypted_bytes[-indices_bytes_size:], dtype=np.int32)

            if len(encrypted_data) <= 16:
                messagebox.showerror("Error", "Invalid encrypted file")
                return

            decrypted_bytes = self.aes_decrypt(encrypted_data, key)
            decrypted_array = np.frombuffer(decrypted_bytes, dtype=np.uint8)
            if decrypted_array.size != indices.size:
                decrypted_array = decrypted_array[:indices.size]

            unscrambled_array = self.unscramble_pixels(decrypted_array, indices, self.original_shape)
            decrypted_image = Image.fromarray(unscrambled_array.astype(np.uint8))

            decrypted_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if not decrypted_path:
                return

            decrypted_image.save(decrypted_path)
            self.display_image(decrypted_path)
            messagebox.showinfo("Success", f"Image decrypted and saved as '{os.path.basename(decrypted_path)}'")
            self.reset_state()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt the image: {e}")

    def reset_state(self):
        self.image_path = ""
        self.is_encrypted = False
        self.image_label.config(image=None, text="Drag and drop an image here or use Browse")
        self.key_entry.delete(0, tk.END)
        self.key_label.config(state=tk.DISABLED)
        self.key_entry.config(state=tk.DISABLED)
        self.encrypt_button.config(state=tk.DISABLED)
        self.decrypt_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = AdvancedImageEncryptionTool()
    app.root.mainloop()

