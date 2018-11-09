#!/usr/bin/python


class Point:
    def __init__(self, pos):
        self.pos = pos

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, val):
        if len(val) > 3:
            raise ValueError('Invalid pos. The length of pos > 3.')
        else:
            self._pos = val

    def __add__(self, other):
        assert len(self.pos) == len(other.pos), 'Dimension mismatch. {}/{}'.format(len(self.pos), len(other.pos))

        res = []
        for i, p in enumerate(self.pos):
            res.append(p + other.pos[i])

        return Point(res)

    def __str__(self):
        return "Point{}".format(tuple(self.pos))


if __name__ == '__main__':

    p1 = Point([1, 2, 3])
    p2 = Point([2, 2, 2])
    print(p1 + p2)

