class BitField:
    def __init__(self, value: int):
        self.value = value

    def __getitem__(self, bit: int):
        return self.value >> bit & 1

    def __setitem__(self, bit: int, state: bool):
        if state:
            self.value |= (1<<bit)
        else:
            self.value &=~ (1<<bit)

    def __int__(self):
        return self.value
