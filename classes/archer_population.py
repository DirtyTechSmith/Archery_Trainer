from .archer import Archer


class ArcherPopulation(object):
    def __init__(self, screen, num_archers=500):
        self._screen = screen
        self.archer_count = num_archers
        self._the_archers = None

    @property
    def the_archers(self):
        """

        Returns:
            dict[int,Archer]:
        """
        if self._the_archers is None:
            self._the_archers = self.makeArchers(num_archers=self.archer_count)

        return self._the_archers

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
            archer_dict[x] = Archer()

        return archer_dict
