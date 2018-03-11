from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "point " + str(self.x) + ", " + str(self.y)

    def dist(self, other):
        """
        distance entre deux points
        :param other:
        :return:
        """
        return sqrt((self.x -other.x)**2 + (self.y - other.y)**2)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __mul__(self, nb):
        return Point(self.x * nb, self.y * nb)

    def __div__(self, nb):
        return Point(float(self.x)/nb, float(self.y)/nb)
