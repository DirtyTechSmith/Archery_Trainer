from vector import Vector

GRAVITY = 9.8

gravity = Vector([0.0, GRAVITY])

grain_to_kilograms = 0.00006479891
kilograms_to_grains = 15432.358


class Arrow(object):

    def __init__(self, position=None, target_position=None, hit_zone_radius=1.0, mass=.03):
        """
        
        Args:
            position(Vector):
            target_position(Vector):
            hit_zone_radius(float): distance in meters away from the target we consider a hit.
            mass (float): mass in kg
        """
        if position is None:
            position = Vector([0.0, 0.0])

        if target_position is None:
            target_position = Vector([0.0, 0.0])

        self._mass = mass
        self._position = position
        self._target_position = target_position
        self.hit_zone_radius = hit_zone_radius  # type:float
        self._move_vector = Vector([0, 0])
        self.in_flight = False  # type: bool
        self.hit_target = False  # type: bool

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
            Vector:

        """
        return self._position

    @position.setter
    def position(self, value):
        """

        Args:
            value (Vector):

        Returns:

        """
        self._position = value

    @property
    def target_position(self):
        """

        Returns:
            Vector:
        """
        return self._position

    @target_position.setter
    def target_position(self, target_pos):
        """

        Args:
            target_pos (Vector):

        """
        self._target_position = target_pos

    @property
    def move_vector(self):
        """

        Returns:
            Vector:
        """
        return self._move_vector

    @move_vector.setter
    def move_vector(self, vector_in):
        """

        Args:
            vector_in (Vector):


        """
        self._move_vector = vector_in

    @property
    def distance_to_target(self):
        """
        current distance from arrow to target

        Returns:
            float:
        """

        return Vector.distance(self.position, self.target_position)

    def fire(self, move_vector):
        """

        Args:
            move_vector (Vector):

        Returns:

        """
        self.in_flight = True
        self.move_vector = move_vector

    def update(self):
        if not self.in_flight:
            return False

        if self.hit_target:
            return False

        self.position


if __name__ == '__main__':
    from archer_log import log
    new_arrow = Arrow(Vector([0.0, 0.0]))
    new_arrow.grains = 300
    log.info(f'grains: {new_arrow.grains}, grams: {new_arrow.mass_grams}, kg : {new_arrow.mass}')
