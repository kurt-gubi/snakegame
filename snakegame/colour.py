import hashlib
from random import Random

def hash_colour(data):
    n = int(hashlib.md5(data.encode('utf-8')).hexdigest(), 16)
    r = Random(n)
    return r.randrange(256), r.randrange(256), r.randrange(256)
