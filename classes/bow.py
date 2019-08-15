from .arrow import Arrow

lbs_to_newtons = 4.4482216282509


class Bow(object):
    def __init__(self, draw_weight_lbs=100.0, draw_length_in=30.0, efficiency=0.9):
        """
        
        Args:
            draw_weight_lbs (float):
            efficiency ():
        """
        self._draw_weight_lbs = draw_weight_lbs
    
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
        newtons = self.
