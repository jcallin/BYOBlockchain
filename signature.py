from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode

def sign(data):
    '''
    Sign data with our local private key and return the signature
    param: string data:     data in string form to sign
    return: b64 signature
    '''
    # Encode the string as bytes for the digest
    bytes_data = data.encode()

    # Import our private key and use it to sign the data
    priv_key = open('key', 'r').read()
    key = RSA.importKey(priv_key)
    signer = PKCS1_v1_5.new(key)
    digest = SHA256.new()
    digest.update(bytes_data)

    signature = signer.sign(digest)

    return b64encode(signature)

def verify_sign(signature, data):
    '''
    Uses a public key to verify that data was signed by a private key
    param: b64 signature:        Signature to be verified
    param: strin  data:          Data that was signed
    return: Boolean. True if the signature is valid; False otherwise.
    '''
    # Encode the string as bytes data for the digest
    bytes_data = data.encode()

    pub_key = open('key.pub', 'r').read()
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(bytes_data)

    if signer.verify(digest, b64decode(signature)):
        return True
    return False
