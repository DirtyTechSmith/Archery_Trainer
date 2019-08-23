from classes.position2d import Position2D

GRAVITY = 9.8

gravity = Position2D([0.0, GRAVITY])

grain_to_kilograms = 0.00006479891
kilograms_to_grains = 15432.358


class Arrow(object):

    def __init__(self, position=None, target_position=None, mass=.03, ):
        """
        
        Args:
            position(Position2D):
            mass (float): mass in kg
        """
        if position is None:
            position = Position2D([0.0, 0.0])

        self._mass = mass
        self._position = position
        self._target_position = target_position
        self.velocity = 0.0  # type: float

    @property
    def mass(self):
        """
        
        Returns:
            float:
        """
        return self._mass

    @mass.setter
    def mass(self, value):
        """
        
        Args:
            value (float):

        Returns:

        """
        self._mass = value

    @property
    def mass_grams(self):
        """
        
        Returns:
            float:
        """
        grams = self.mass * 1000.0
        return grams

    @mass_grams.setter
    def mass_grams(self, value):
        """
        
        Args:
            value (float):

        """
        kg = value / 1000.0
        self.mass = kg

    @property
    def grains(self):
        """
        weight of arrow in grains
        Returns:
            float:
        """
        grain_weight = self.mass * kilograms_to_grains
        return grain_weight

    @grains.setter
    def grains(self, value):
        """
        
        Args:
            value (float):

        """
        kgs = value * grain_to_kilograms
        self.mass = kgs

    @property
    def position(self):
        """

        Returns:
            Position2d:
        """
        return self._position

    @position.setter
    def position(self, value):
        """

        Args:
            value (Position2D):

        Returns:

        """
        self._position = value

    @property
    def target_position(self):
        """

        Returns:
            Position2d:
        """
        return self._position

    @target_position.setter
    def target_position(self, target_pos):
        """

        Args:
            target_pos (Position2D): 

        """
        self._target_position = target_pos


if __name__ == '__main__':
    new_arrow = Arrow(Position2D([0.0, 0.0]))
    new_arrow.grains = 300
    print(f'grains: {new_arrow.grains}, grams: {new_arrow.mass_grams}, kg : {new_arrow.mass}')
