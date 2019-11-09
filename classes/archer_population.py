from .archer import Archer
from .entity import Entity
from pygame import Surface
from vector import Vector
import random
import tensorflow as tf

Dense = tf.keras.layers.Dense


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

    def mutateLayer(self, layer, mutation_rate=1.5, mut_min=-.01, mut_max=0.01):
        """

        Args:
            layer (Dense):
            mutation_rate(float):
            mut_min(float):
            mut_max(float):
        Returns:
            Dense:
        """
        for index, value in enumerate(layer.weights):

            mutation_check = random.uniform(0.0, 100.0)
            if mutation_check > mutation_rate:
                continue

            # print('IMA MUTIN BRO')
            mutate_amount = random.uniform(mut_min, mut_max)
            value.assign(value + mutate_amount)
            # if value > 1.0:
            #     value = 1.0
            #
            # elif value < -1.0:
            #     value = -1.0

            layer.weights[index] = value

        mutation_check = random.uniform(0.0, 100.0)
        if mutation_check <= mutation_rate:
            mutate_amount = random.uniform(mut_min, mut_max)
            layer.bias.assign(layer.bias + mutate_amount)

        return layer

    def breedPopulation(self):
        the_misses = [archer.miss for archer in self.archers.values()]
        biggest_miss = max(the_misses)
        closest_hit = min(the_misses)
        # print(f'biggest miss: {biggest_miss}, closest hit: {closest_hit}')
        # lets determine our fitness
        for archer in self.archers.values():
            if archer.miss == 0:
                archer.fitness = 1.0
                print('WE GOT A STRONK BOI')
                continue

            normalized_miss = archer.miss / biggest_miss
            fitness = 1.0 - normalized_miss
            archer.fitness = fitness

        # ok now lets store off the weights and biases for chosing
        num_archers = len(self.archers.keys())
        # 0 is weighting, 1 is values
        hidden_1_bias_weighting = [list(range(num_archers)), list(range(num_archers))]  # type: list[list]
        hidden_2_bias_weighting = [list(range(num_archers)), list(range(num_archers))]  # type: list[list]
        hidden_1 = []
        hidden_2 = []

        for archer_id, archer in self.archers.items():
            hidden_1_bias_weighting[0][archer_id] = archer.fitness
            hidden_1_bias_weighting[1][archer_id] = archer.brain.hidden_1.bias
            hidden_2_bias_weighting[0][archer_id] = archer.fitness
            hidden_2_bias_weighting[1][archer_id] = archer.brain.hidden_2.bias

            for index, value in enumerate(archer.brain.hidden_1.weights):
                hidden_1.append([list(range(num_archers)), list(range(num_archers))])
            for index, value in enumerate(archer.brain.hidden_2.weights):
                hidden_2.append([list(range(num_archers)), list(range(num_archers))])

            for index, value in enumerate(archer.brain.hidden_1.weights):
                hidden_1[index][0][archer_id] = archer.fitness
                hidden_1[index][1][archer_id] = value

            for index, value in enumerate(archer.brain.hidden_2.weights):
                hidden_2[index][0][archer_id] = archer.fitness
                hidden_2[index][1][archer_id] = value

        for archer_id, archer in self.archers.items():
            my_hidden_1_bias = random.choices(hidden_1_bias_weighting[1], weights=hidden_1_bias_weighting[0])[0]

            # print(archer.brain.hidden_1.bias.shape)
            # print(my_hidden_1_bias.shape)
            archer.brain.hidden_1.bias.assign(my_hidden_1_bias)
            my_hidden_2_bias = random.choices(hidden_2_bias_weighting[1], weights=hidden_2_bias_weighting[0])[0]
            archer.brain.hidden_2.bias.assign(my_hidden_2_bias)
            for index, weight in enumerate(archer.brain.hidden_1.weights):
                chances = hidden_1[index][0]
                values = hidden_1[index][1]
                current_weights = random.choices(values, weights=chances)[0]
                weight.assign(current_weights)

        # we determined fitness and breed, now for mutation
        for archer in self.archers.values():
            archer.brain.hidden_1 = self.mutateLayer(archer.brain.hidden_1)
            archer.brain.hidden_2 = self.mutateLayer(archer.brain.hidden_2)
