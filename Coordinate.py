from pygame import math


class Coordinate():
    """
    Simple 2-D integer coordinate class
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def straight_line_distance(self, other):
        if self.x == other.x:
           return math.abs(self.y - other.y)
        elif self.y == other.y:
           return math.abs(self.x - other.x)
        else:
           return 0

    def is_greater_than(self, other):
        if self.x == other.x:
           return self.y > other.y
        elif self.y == other.y:
           return self.x > other.x
        else:
           return False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def is_legal(self):
        return self.x >= 0 and self.x < 9 and self.y >= 0 and self.y < 9