import math


class Position2D(object):
    def __init__(self, position_list):
        """

        Args:
            position_list (list[int or float]):
        """
        self._position_list = position_list

    @property
    def position_list(self):
        """

        Returns:
            list[int or float]:
        """
        return self._position_list

    @property
    def x(self):
        """

        Returns:
            int or float:
        """
        return self.position_list[0]

    @x.setter
    def x(self, value):
        """

        Args:
            value (int or float):


        """
        self.position_list[0] = value

    @property
    def y(self):
        """

        Returns:
            int or float:
        """
        return self.position_list[1]

    @y.setter
    def y(self, value):
        """

        Args:
            value (int or float):


        """
        self.position_list[1] = value

    @property
    def length(self):
        """

        Returns:
            float:
        """
        pos_sums = (self.x * self.x) + (self.y * self.y)

        length = math.sqrt(pos_sums)
        return length

    @staticmethod
    def sum(position_1, position_2):
        """

        Args:
            position_1 (Position2D):
            position_2 (Position2D):

        Returns:
            Position2D:
        """
        pos_list = [position_1.x + position_2.x, position_1.y + position_2.y]
        new_pos = Position2D(pos_list)
        return new_pos

    def increase(self, other_pos):
        """

        Args:
            other_pos (Position2D):

        """
        self = self.sum(self, other_pos)
        return

    def scalarMultiplication(self, scalar):
        """

        Args:
            scalar (float):

        Returns:

        """
        self.x *= scalar
        self.y *= scalar

    def copy(self):
        """

        Returns:
            Position2D:
        """
        new_pos = Position2D([self.x, self.y])
        return new_pos

    @staticmethod
    def subract(position_1, position_2):
        """

        Args:
            position_1 (Position2D):
            position_2 (Position2D):

        Returns:
            Position2D:
        """
        new_list = [position_2.x - position_1.x, position_2.y - position_1.y]
        new_pos = Position2D(new_list)
        return new_pos

    @staticmethod
    def distance(position_1, position_2):
        """

        Args:
            position_1 ():
            position_2 ():

        Returns:
            float:
        """

        sum = (math.pow((position_1.x - position_2.x), 2)) + (math.pow((position_1.y - position_2.y), 2))
        distance = math.sqrt(sum)
        return distance

    def __str__(self):
        new_str = f'{self.x}, {self.y}'
        return new_str


if __name__ == '__main__':
    new_pos = Position2D([3, 2])
    print(new_pos)
    print(new_pos.length)
    pos_2 = Position2D([3, 7])
    dist = Position2D.distance(new_pos, pos_2)
    print(dist)
    pos_2.scalarMultiplication(2.0)
    print(pos_2)
    print(pos_2.length)