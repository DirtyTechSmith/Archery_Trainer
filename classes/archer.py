import math
import tensorflow as tf
import pygame
import random
from classes.position2d import Position2D

MAX_BOW_STR = 100.0


class ArcherBrain(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(5, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(3, activation=tf.nn.softmax)

    def call(self, inputs):
        """

        Args:
            inputs (list[float]):

        Returns:
            list[float]
        """
        inputs = tf.convert_to_tensor([inputs])
        x = self.dense1(inputs)
        return self.dense2(x)


class Archer(object):
    def __init__(self, position, screen, screen_size, bow_str=100.0, brain=None):
        """

        Args:
            position (list[float]):
            screen():
            screen_size(list[int]):
            bow_str ():
            brain(ArcherBrain):
        """
        self._bow_str = bow_str
        self._brain = brain
        self._position = Position2D(position)
        self.screen = screen
        self._screen_size = Position2D(screen_size)

    @property
    def position(self):
        """

        Returns:
            Position2D:
        """
        return self._position

    @property
    def screen_size(self):
        """

        Returns:
            Position2D:
        """

        return self._screen_size

    @property
    def relative_position(self):
        """

        Returns:
            list[float]:
        """
        relative_pos = [float(self.position.x / self.screen_size.x), float(self.position.y / self.screen_size.y)]
        return relative_pos

    @property
    def brain(self):
        """

        Returns:
            ArcherBrain:
        """
        if self._brain is None:
            self._brain = self.createBrain()

        return self._brain

    @staticmethod
    def createBrain():
        """

        Returns:
            ArcherBrain:
        """
        the_brain = ArcherBrain()
        return the_brain

    def calculate_relative_pos(self, pos):
        """

        Args:
            pos (list[int]):

        Returns:
            list[float]:
        """

    def shoot(self, enemy_position):
        """

        Args:
            enemy_position ():

        Returns:

        """
        enemy_position = Position2D(enemy_position)
        inputs = [self.position.x, self.position.y, enemy_position.x, enemy_position.y, self._bow_str]
        results = self.brain.call(inputs)  # type: tf.Tensor
        the_list = [float(thing) for thing in results[0]]
        arrow_speed = the_list[2] * self._bow_str
        target_position = Position2D([the_list[0], the_list[1]])
        print(target_position)

        target_position = target_position.scalarMultiplication(arrow_speed)
        print(target_position)

        import random
        start_pos = self.position.position_list
        end_pos = [random.randint(0, self.screen_size.x), random.randint(0, self.screen_size.y)]
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.line(self.screen, color, start_pos, end_pos)
