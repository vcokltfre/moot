from time import time


class IDGenerator():
    def __init__(self):
        self.inc = 0

    def next(self):
        t = round(time() * 1000) - 1609459200000
        self.inc += 1
        return ((t << 14) | (1 << 6) | (self.inc % 2**6))
