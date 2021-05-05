from time import time


class IDGenerator():
    def __init__(self):
        self.inc = 0

    def next(self):
        t = round(time() * 1000) - 1609459200000
        self.inc += 1
        return ((t << 14) | (1 << 6) | (self.inc % 2**6))


def decode_sf(sf: int) -> tuple:
  t = (sf & ((1 << 64) - 1)) >> 14  # Timestamp
  w = (sf & ((1 << 14) - 1)) >> 6   # Worker ID
  i = (sf & ((1 << 6) - 1)) >> 0    # Increment
  return (t, w, i)
