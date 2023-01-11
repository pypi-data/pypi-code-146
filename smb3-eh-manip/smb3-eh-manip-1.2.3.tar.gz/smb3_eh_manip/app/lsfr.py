INITIAL_SEED = [0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]


class LSFR:
    def __init__(self, data=None):
        self.data = list(INITIAL_SEED) if not data else data

    def clone(self):
        return LSFR(list(self.data))

    def get(self, byte):
        return self.data[byte]

    def next_n(self, iterations):
        for _x in range(iterations):
            self.next()

    def next(self):
        temp = self.data[0] & 0x2
        carry = not not ((self.data[1] & 0x2) ^ temp)
        for i, rng_byte in enumerate(self.data):
            b = rng_byte & 1
            self.data[i] = (carry << 7) | (rng_byte >> 1)
            carry = b
        return self.data

    def random_n(self, offset=0):
        # RandomN is the value most of the code uses or indexes off of.
        # It is the second byte in the array.
        # HB directions use an offset for which index they are, e.g.
        # w1 bro is index 2 so wed look in data[1+2], or the 4th byte
        return self.data[1 + offset]

    def hand_check(self):
        # returns True if a hand grabs the player, False otherwise
        return self.random_n() & 0x1 == 0
