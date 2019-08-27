from .arrow import Arrow
from vector import Vector
import numpy

LBS_TO_NEWTONS = 4.4482216282509
INCHES_TO_METERS = 0.0254


class Bow(object):
    def __init__(self, archer=None, arrow_velocity=60.0, draw_weight_lbs=100.0, draw_length=0.75, efficiency=1.0, arrow_type=None):
        """

        Args:
            archer(classes.archer.Archer):
            arrow_velocity (float):
            draw_weight_lbs (float):
            draw_length (float):
            efficiency (float):
            arrow_type (Arrow):
        """
        if arrow_type is None:
            arrow_type = Arrow

        self._archer = archer

        self._draw_weight_lbs = draw_weight_lbs
        self._draw_length = draw_length
        self._arrow_velocity = arrow_velocity
        self._arrow_type = arrow_type
        self._shot_arrows = []
        self._efficiency = efficiency

    @property
    def archer(self):
        """
        the archer shooting the bow.

        Returns:
            classes.archer.Archer:
        """

        return self._archer

    @archer.setter
    def archer(self, the_archer):
        """

        Args:
            the_archer (classes.archer.Archer):

        Returns:

        """
        self._archer = the_archer

    @property
    def draw_weight_lbs(self):
        """
        
        Returns:
            float:
        """
        return self._draw_weight_lbs

    @property
    def newton_force(self):
        """
        
        Returns:
            float:
        """
        newtons = self.draw_weight_lbs * LBS_TO_NEWTONS
        return newtons

    @property
    def arrow_velocity(self):
        """
        how fast this bow will shoot an arrow in meters/sec

        Returns:
            float:
        """
        return self._arrow_velocity

    @property
    def draw_length(self):
        """Draw length in meters

        Returns:
            float:
        """
        return self._draw_length

    @property
    def efficiency(self):
        """ How efficient the bow is
        based on a 0.0 - 1.0 value
        bow with
        Returns:
            float:
        """
        return self._efficiency

    def shootArrow(self, vector, pull_percent, target_position):
        """

        Args:
            vector (Vector):
            pull_percent (float):
            target_position(Vector):

        Returns:
            Arrow:
        """
        new_arrow = Arrow(position=self.archer.position)

        self._shot_arrows.append(new_arrow)
