import time


class Randomf:
    __slots__ = ["seed"]

    def __init__(self, seed: int = None):
        if seed is None:
            self.seed = int(time.time())
        elif isinstance(seed, int):
            self.seed = seed
        else:
            raise TypeError("seed should be int")

    def __repr__(self):
        return f"<Random ({hex(self.seed)})>"

    def next_int(self):
        new_seed = (self.seed * 0x5DEECE66D + 0xB) & 0xFFFFFFFFFFFF
        i = (new_seed >> 16)

        return i, Randomf(new_seed)

    def next_non_negative_int(self):
        i, r = self.next_int()
        return i if i > 0 else (-i + 1), r

    def next_double(self):
        i, r = self.next_non_negative_int()
        return i / (0x7FFFFFFF + 1), r

    def next_boolean(self):
        i, r = self.next_non_negative_int()
        return i % 2 == 0, r

    @staticmethod
    def next_int_in_range(low, high):
        """represent [low, high)"""
        def _(random):
            i, r = random.next_non_negative_int()
            return low + (i % (high - low)), r

        return _

    def next_lower_letter(self):
        lower_case = self.next_int_in_range(97, 123)
        i, r = lower_case(self)
        return chr(i), r

    def next_upper_letter(self):
        upper_case = self.next_int_in_range(65, 91)
        i, r = upper_case(self)
        return chr(i), r

    def seq(self, func, num=1):
        """
        :param func: Random => (A, Random)
        :param num: length of seq
        :return: ([A1, A2, ..., An], Random)
        """
        record = []
        cur = self
        while num > 0:
            v, r = func(cur)
            record.append(v)
            cur = r
            num -= 1
        return record, cur
