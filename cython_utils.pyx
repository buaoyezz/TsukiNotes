'''
CREATED ON: 2024
FOR TSUKINOTES
8/22 --> ZZBUAOYE
'''

from libc.string cimport memset

def format_chunk(chunk):
    cdef int i
    cdef list formatted_hex = []
    cdef str formatted_str
    for i in range(len(chunk)):
        formatted_hex.append("%02x" % chunk[i])
    formatted_str = " ".join(formatted_hex)
    return formatted_str

def read_file_in_chunks(filename, chunk_size=1024):
    cdef list chunks = []
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunks.append(format_chunk(chunk))
    return chunks

# Please Look Set_up.py At First