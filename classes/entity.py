from vector import Vector


class Entity(object):
    def __init__(self, position):
        """

        Args:
            position (Vector):
        """

        self.position = position

    @property
    def position(self):
        """

        Returns:
            Vector:
        """