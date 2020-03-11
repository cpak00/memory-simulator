import numpy as np
from core.io import IO

def bits2dtype(bits):
    if bits <= 8:
        bits = 8
        dtype = np.uint8
    elif bits <= 16:
        bits = 16
        dtype = np.uint16
    elif bits <= 32:
        bits = 32
        dtype = np.uint32
    elif bits <= 64:
        bits = 64
        dtype = np.uint64
    else:
        raise Exception("too much bits (require: <= 64)")

    return dtype

def hamming_distance(x):
    d = 0
    s = str(bin(x))
    for i in range(2, len(s)):
        if int(s[i]) is 1:
            d += 1
    return d

def cycle_left_shifting(raw, bits, n):
    if n == 0:
        return raw
    
    raw = (bin(raw))[2:]
    raw = '0' * (bits - len(raw)) + raw
    return int(raw[n:] + raw[:n], 2)

def cycle_right_shifting(raw, bits, n):
    return cycle_left_shifting(raw, bits, -n)

def batchIO_write(data):
    io = IO()
    for times in range(len(data)):
        for row in range(len(data[times])):
            io.push_write(row, data[times][row])

    return io


