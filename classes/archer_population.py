from .archer import Archer


class ArcherPopulation(object):
    def __init__(self, num_archers=500):
        self._the_archers = {}

    @property
    def the_archers(self):
        """

        Returns:
            dict[int,]:
        """
        return self._the_archers
