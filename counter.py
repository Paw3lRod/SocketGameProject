class Counter:
    def __init__(self, length, start) -> None:
        self.index = start
        self.length = length

    def inc(self):
        self.index += 1
        if (self.index > (self.length - 1)):
            self.index = 0

    def dec(self):
        self.index -= 1
        if (self.index < 0):
            self.index = (self.length - 1)
