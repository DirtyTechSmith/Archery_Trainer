import random
from threading import Thread

import pygame
import tensorflow as tf
from pygame import Surface

from classes.bow import Bow
from classes.entity import Entity
from vector import Vector

MAX_BOW_STR = 275.0


class ArcherBrain(tf.keras.Model):
    def compute_output_signature(self, input_signature):
        pass

    def __init__(self, brain_cells=32):
        super().__init__()
        self.input_2d = tf.keras.layers.Dense(5, activation=tf.nn.sigmoid)
        self.hidden_1 = tf.keras.layers.Dense(brain_cells, activation=tf.nn.relu)
        self.hidden_2 = tf.keras.layers.Dense(brain_cells, activation=tf.nn.relu)
        self.output_2d = tf.keras.layers.Dense(3, activation=tf.nn.softmax)

    def calculate_trajectory(self, inputs):
        """

        Args:
            inputs (list[float]):

        Returns:
            list[float]
        """
        inputs = tf.convert_to_tensor([inputs])
        x = self.input_2d(inputs)
        x = self.hidden_1(x)
        x = self.hidden_2(x)
        return self.output_2d(x)


class Archer(Entity, Thread):
    def __init__(self, position, screen, target, bow_str=MAX_BOW_STR, arrow_count=1, brain=None):
        """

        Args:
            position (Vector):
            screen(Surface):
            target(Entity):
            bow_str (float):
            arrow_count(int):
            brain(ArcherBrain):
        """

        Thread.__init__(self)
        super().__init__(position, screen)
        self._bow_str = bow_str
        self._bow = Bow(arrow_velocity=self.bow_str)
        self._brain = brain
        self._target = target
        self.arrow_count = arrow_count
        self.arrows_fired = []
        self.miss = float('inf')
        self.fitness = 0

    @property
    def bow_str(self):
        """
        arrow velocity in meters/s

        Returns:
            float:
        """
        return self._bow_str

    @property
    def bow(self):
        return self._bow

    @property
    def target(self):
        """

        Returns:
            Entity:
        """
        return self._target

    @property
    def relative_position(self):
        """

        Returns:
            list[float]:
        """
        relative_pos = [float(self.position.x / self.screen.get_width()),
                        float(self.position.y / self.screen.get_height())]
        return relative_pos

    @property
    def brain(self):
        """

        Returns:
            ArcherBrain:
        """
        if self._brain is None:
            self._brain = self.create_brain()

        return self._brain

    @staticmethod
    def create_brain():
        """

        Returns:
            ArcherBrain:
        """
        the_brain = ArcherBrain()
        return the_brain

    def reset_miss(self):
        """ we want to reset the miss to an infinite miss

        Returns:
            float:
        """
        self.miss = float('inf')

    def calculate_relative_position(self, pos):
        """

        Args:
            pos (list[int]):

        Returns:
            list[float]:
        """

    def shoot(self, enemy=None):
        """

        Args:
            enemy (entity):

        Returns:
            float:
        """
        if enemy is None:
            enemy = self.target

        enemy_position = enemy.position

        gravity = Vector([0.0, 9.8])

        inputs = [self.position.x, self.position.y, self.target.position.x, self.target.position.y, self.bow_str]

        results = self.brain.calculate_trajectory(inputs)  # type: tf.Tensor
        the_list = [float(thing) for thing in results[0]]
        bow_pullback = the_list[2]
        bow_pullback = abs(bow_pullback)
        arrow_speed = self.bow_str * bow_pullback

        arrow_vector = Vector([the_list[0], (0.0 - the_list[1])])
        # arrow_vector = Vector([the_list[0], the_list[1]])
        arrow_vector.normalize()

        arrow_vector *= arrow_speed

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        start_pos = self.position
        last_pos = self.position.copy()
        counter = 0

        while last_pos.y <= self.screen.get_height():
            # sleep(.1)
            new_pos = last_pos + arrow_vector

            draw_arrow = True
            if new_pos.x >= self.screen.get_width():
                draw_arrow = False
            # if new_pos.x >= self.target.position.x:
            #     draw_arrow = False

            if new_pos.y >= self.screen.get_height():
                break

            # if new_pos.y >= self.target.position.y:
            #     break

            if draw_arrow:
                pygame.draw.line(self.screen, color, last_pos.float_list, new_pos.float_list)

            last_pos = new_pos.copy()
            arrow_vector += gravity

        # end_pos = Vector.sum(start_pos, arrow_vector)
        miss = Vector.distance(last_pos, enemy_position)
        # print(f'I missed by this much: {miss}')
        # reward =  missToRewardFn(miss)
        # self.Reward(reward)

        return miss

    # def reward(self, ):

    def run(self):
        for x in range(self.arrow_count):
            result = self.shoot(self.target)
            self.arrows_fired.append(result)

        closest_shot = min(self.arrows_fired)
        if closest_shot < self.miss:
            self.miss = closest_shot

    def volley(self):
        self.run()

    def volley_threaded(self):
        self.start()

    def wait_for_fire(self):
        self.join()
