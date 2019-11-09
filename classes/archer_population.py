from .archer import Archer
from .entity import Entity
from pygame import Surface
from vector import Vector


class ArcherPopulation(object):
    def __init__(self, screen, archer_pos, target, num_archers=500, ):
        """

        Args:
            screen (Surface):
            archer_pos(Vector):
            num_archers (int):
            target (Entity):
        """
        self._screen = screen
        self.archer_count = num_archers
        self._archers = None
        self.target = target
        self.archer_position = archer_pos

    @property
    def archers(self):
        """

        Returns:
            dict[int,Archer]:
        """
        if self._archers is None:
            self._archers = self.makeArchers(num_archers=self.archer_count)

        return self._archers

    def makeArchers(self, num_archers=None):
        """

        Args:
            num_archers (int):

        Returns:
            dict[int,Archer]:
        """
        if num_archers is None:
            num_archers = self.archer_count

        archer_dict = {}
        for x in range(num_archers):
            archer_dict[x] = Archer(self.archer_position.copy(), self._screen, self.target)

        return archer_dict

    def volley(self):
        for archer_number, archer in self.archers.items():
            archer.volley()

    def volleyThreaded(self):
        for archer_number, archer in self.archers.items():
            archer.volley_Threaded()
            archer.waitForFire()

    def breedPopulation(self):
        the_misses = [archer.miss for archer in self.archers.values()]
        biggest_miss = max(the_misses)
        closest_hit = min(the_misses)
        print(f'biggest miss: {biggest_miss}, closest hit: {closest_hit}')
        for archer in self.archers.values():
            pass
