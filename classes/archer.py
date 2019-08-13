import tensorflow as tf
import pygame

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
        self._position = position
        self._screen_size = screen_size

    @property
    def position(self):
        """

        Returns:
            list[int]:
        """
        return self._position

    @property
    def screen_size(self):
        """

        Returns:
            list[int]:
        """
        return self._screen_size

    @property
    def relative_position(self):
        """

        Returns:
            list[float]:
        """
        relative_pos = [float(self.position[0] / self.screen_size[0]), float(self.position[1] / self.screen_size[1])]

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
