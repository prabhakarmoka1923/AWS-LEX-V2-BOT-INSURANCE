"""module to decrypt any encrypted value"""

import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def get_private_key(private_key_content, password=None):
    """Get private key from PEM file"""
    return serialization.load_pem_private_key(private_key_content.encode('utf-8'),
                                              password=password)


def format_private_key(key: str):
    """
        method to format the public key passed
    """
    if key.count("\n") > 0:
        return key
    # public_key_version = key[0:key.find("-----")]
    prefix = "-----BEGIN RSA PRIVATE KEY-----"
    suffix = "-----END RSA PRIVATE KEY-----"
    raw_data = key.replace(prefix, "").replace(suffix, "").replace(" ", "")
    chunksize = 65
    segments = [raw_data[i:i + chunksize] for i in range(0, len(raw_data), chunksize)]
    return prefix + "\n" + "\n".join(segments) + "\n" + suffix


class Decrypter:
    """Decryption utility class"""

    def __init__(self, private_key, password=None):
        """Decrypter with a private key file"""
        self.private_key_content = format_private_key(private_key)
        self.private_key = get_private_key(self.private_key_content, password)

    def _decrypt(self, encrypted_message):
        """Decrypt an encrypted message with private key"""
        return self.private_key.decrypt(
            base64.b64decode(encrypted_message),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def decrypt_chunk(self, encrypted_message):
        """Decrypt an encrypted long message with private key"""
        chunk_size = 344  # chunk size: b64 encoding of 256 chars (342 + '==')
        number_of_chunks = len(encrypted_message) // chunk_size  # note: always integer chunks
        res = [self._decrypt(encrypted_message[(cn - 1) * chunk_size: cn * chunk_size])
               for cn in range(1, number_of_chunks + 1)]
        return res

    def decrypt(self, encrypted_message):
        '''
            create a single message from chunks
        '''
        res = self.decrypt_chunk(encrypted_message)
        result = res[0]
        if len(res) != 1:
            result = ''.join(val for val in res)
        return result
