from vector import Vector
from collections import Iterable
from pygame import Surface


class Entity(object):
    def __init__(self, position, screen):
        """

        Args:
            position (Vector):
            screen(Surface):
        """

        self._position = position
        self.screen = screen

    @property
    def position(self):
        """

        Returns:
            Vector:
        """
        return self._position

    @property
    def position_tuple(self):
        """

        Returns:
            tuple(float):
        """
        return tuple(self.position)

    @property
    def screen_size(self):
        """

        Returns:
            Vector:
        """
        size = [self.screen.get_width(), self.screen.get_height()]
        return size
