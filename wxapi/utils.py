import hashlib


def to_bytes(text):
    """ 转成bytes"""
    if isinstance(text, str):
        text = text.encode('utf8')
    return text


def to_string(text):
    """ 转成string"""
    if isinstance(text, bytes):
        text = text.decode('utf8', 'ignore')
    return text


def make_sha1_hash(text):
    """ sha1加密"""
    sha1_hash = hashlib.sha1(to_bytes(text)).hexdigest()
    return sha1_hash
    
