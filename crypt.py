#imports
import random
#froms
from cryptography.fernet import Fernet


def encrypt_string(data, key=None):
    # Check if the input 'data' is a string. If so, encode it to bytes.
    # Otherwise, assume it's already bytes (e.g., from file.read() in binary mode).
    if isinstance(data, str):
        data_in_bytes = data.encode('utf-8')
    elif isinstance(data, bytes):
        data_in_bytes = data
    else:
        # Raise an error for unexpected input types to ensure robustness
        raise TypeError("Input data for encryption must be a string or bytes.")

    return_key = None
    if key is None:
        key = Fernet.generate_key()

        #save key to file
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        if isinstance(key, str):
            return_key = key.decode('utf-8')
        elif isinstance(key, bytes):
            return_key = key

    f = Fernet(key)

    return_token = None
    return_token = f.encrypt(data_in_bytes)

    return (return_key, return_token)

def decrypt_string(key, token):
    # Ensure the key is in bytes format for Fernet
    if isinstance(key, str):
        key_bytes = key.encode('utf-8')
    elif isinstance(key, bytes):
        key_bytes = key
    else:
        raise TypeError("Key for decryption must be a string or bytes.")

    # Ensure the token is in bytes format for Fernet
    if isinstance(token, str):
        token_bytes = token.encode('utf-8')
    elif isinstance(token, bytes):
        token_bytes = token
    else:
        raise TypeError("Token for decryption must be a string or bytes.")

    # Decrypt and then decode the result back to a string
    return Fernet(key_bytes).decrypt(token_bytes).decode('utf-8')

# Removes the salt from the end of a password string
def unsalt_data(data, salt):
    pos = data.find(salt)

    for i in range(len(salt)):
        if data[pos+i]==salt[i]:
            pass
        else:
            return False # Salt is invalid
    return data[0:pos-1]