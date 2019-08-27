from vector import Vector
from collections import Iterable

class Entity(object):
    def __init__(self, position):
        """

        Args:
            position (Vector or Iterable[float]):
        """
        if isinstance(position,Iterable):
            position = Vector(position)

        self._position = position

    @property
    def position(self):
        """

        Returns:
            Vector:
        """
        return self._position
