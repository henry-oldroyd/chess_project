from hashlib import sha256

# this hash function produces an integer hash of a python object
# it is necessary as the in built hash function produces different hashes for the same object, 
# this function always produces the same hash for a given object, this allows the hash to be stored in a database for later use
def safe_hash(item):
    # https://stackoverflow.com/questions/30585108/disable-hash-randomization-from-within-python-program

    # convert item (usually tuple) to string
    encoded_string = repr(item).encode("utf-8")
    # produce a hexadecimal string hash of the object
    hex_hash = sha256(encoded_string).hexdigest()
    # convert this to an integer
    # int_hash = int(hex_hash, 16)
    # return int_hash
    return hex_hash
