from config import config

class Coder(object):
    def __init__(self):
        self.mm = None
        return

    def bind(self, mm):
        self.mm = mm
        return

    def encode(self, addr, raw):
        return raw
    
    def decode(self, addr, raw):
        return raw
    
    pass