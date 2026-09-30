"""Encryption logic using asymmetric encryption"""

import base64
import math

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend


def get_public_key(public_key_content):
    """Get public key from PEM file"""
    return serialization.load_pem_public_key(public_key_content.encode('utf-8'))


class Encrypter:
    """Encryption utility class"""

    def __init__(self, public_key_version, public_key_data):
        """Encrypter with a public key file"""
        self.public_key_version = public_key_version
        self.public_key = get_public_key(public_key_data)

    def _encrypt(self, message):
        """Encrypt a short message with public key and padding"""
        return self.type_specific_encryption(message)

    def type_specific_encryption(self, message):
        """Wrapper function to encrypt the message based on type, it might be string/bytes"""
        if isinstance(message, str):
            message = message.encode('utf-8')
        return base64.b64encode(self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ))

    def encrypt(self, message):
        """Join encrypted chunks with public_key_version and return encrypted message"""
        res = self.encrypt_chunk(message)
        encrypted_value = ''.join(val.decode('ascii') for val in res)
        return self.public_key_version + "_" + encrypted_value

    def encrypt_chunk(self, message):
        '''
            Divide message into chunks and encrypt
        '''
        chunk_size = 190  # chunk size SHA-256 has overhead of 66
        number_of_chunks = math.ceil(len(message) / chunk_size)
        res = [self._encrypt(message[(cn - 1) * chunk_size: cn * chunk_size])
               for cn in range(1, number_of_chunks + 1)]
        return res
class SymmetricEncrypter:
    """Symmetric encrypter using AES"""

    def __init__(self, key):
        """Initiatialize based on key and set up ciphers and such"""
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        self.encryptor = cipher.encryptor()
        self.decryptor = cipher.decryptor()
        self.padder = PKCS7(algorithms.AES.block_size).padder()
        self.unpadder = PKCS7(algorithms.AES.block_size).unpadder()

    def encrypt(self, plaintext):
        """Encrypt using key and ensure padding"""
        sym_enc_prefix = "symenc:"
        padder, encryptor = self.padder, self.encryptor
        plaintext = plaintext.encode()
        padded_data = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        encodedciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return sym_enc_prefix + encodedciphertext

    def decrypt(self, ciphertext):
        """Decrypt using cipher and take into account padding"""
        if not isinstance(ciphertext, str):
            ciphertext = ciphertext.decode('utf-8')
        unpadder, decryptor = self.unpadder, self.decryptor
        decodedciphertext = base64.b64decode(ciphertext)
        padded_data = decryptor.update(decodedciphertext) + decryptor.finalize()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext.decode('utf-8')
