import struct

from util.tool import cycle_left_shifting, cycle_right_shifting, hamming_distance

class DataParser(object):
    '''
    parse float into format of unsigned integer\n
    and do some bitwise operation like cycle shifting
    '''
    def __init__(self, bits):
        self.bits = bits
        return


    def float2hex(self, origin):
        s = ''
        if self.bits == 32:
            s = struct.pack('<f', origin).hex()
        elif self.bits == 64:
            s = struct.pack('<d', origin).hex()
        else:
            raise Exception('only 32bits or 64bits can be encoded as float32/double64')
        return int(s, 16)

    def hex2float(self, origin):
        if self.bits == 32:
            origin = '{:0>8x}'.format(origin)
            s = struct.unpack('<f', bytes.fromhex(origin))[0]
        elif self.bits == 64:
            origin = '{:0>16x}'.format(origin)
            s = struct.unpack('<d', bytes.fromhex(origin))[0]
        else:
            raise Exception('only 32bits or 64bits can be decoded as float32/double64')
        return s

    def bcs_l(self, raw, n):
        return cycle_left_shifting(raw, self.bits, n)

    def bcs_r(self, raw, n):
        return cycle_right_shifting(raw, self.bits, n)

    def hamming(self, x):
        return hamming_distance(x)

    pass
