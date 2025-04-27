import base64
import binascii
import string

def decode_base64(data: str) -> str:
    """Decode base64 string"""
    return base64.b64decode(data).decode()

def encode_base64(data: str) -> str:
    """Encode string to base64"""
    return base64.b64encode(data.encode()).decode()

def hex2bin(hex_str: str) -> bytes:
    """Convert hex string to bytes"""
    return binascii.unhexlify(hex_str)

def get_charset() -> str:
    """Get common charset for brute forcing"""
    return string.ascii_letters + string.digits