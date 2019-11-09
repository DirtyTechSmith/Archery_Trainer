import math
import tensorflow as tf
import pygame
from pygame import Surface
import random
from time import sleep
from vector import Vector
from classes.bow import Bow
from classes.entity import Entity
from threading import Thread
from collections import Iterable

MAX_BOW_STR = 300.0


class ArcherBrain(tf.keras.Model):
    def compute_output_signature(self, input_signature):
        pass

    def __init__(self):
        super().__init__()
        self.input_2d = tf.keras.layers.Dense(5, activation=tf.nn.sigmoid)
        self.hidden_1 = tf.keras.layers.Dense(32, activation=tf.nn.relu)
        self.hidden_2 = tf.keras.layers.Dense(32, activation=tf.nn.relu)
        self.output_2d = tf.keras.layers.Dense(3, activation=tf.nn.softmax)

    def calculateTrajectory(self, inputs):
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
        relative_pos = [float(self.position.x / self.screen.get_width()), float(self.position.y / self.screen.get_height())]
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

    def resetMiss(self):
        self.miss = float('inf')

    def calculate_relative_pos(self, pos):
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
        # print(inputs)
        results = self.brain.calculateTrajectory(inputs)  # type: tf.Tensor
        the_list = [float(thing) for thing in results[0]]
        # print(f'bow pullback: {the_list[2]}')
        bow_pullback = the_list[2]
        arrow_speed = self.bow_str * bow_pullback

        arrow_vector = Vector([the_list[0], (0.0 - the_list[1])])
        arrow_vector.normalize()
        # print(arrow_vector)

        arrow_vector *= arrow_speed

        # print(arrow_vector)


        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        start_pos = self.position
        # print(f'self.postion:{self.position}')
        last_pos = self.position.copy()
        counter = 0
        # print(f'last pos:{last_pos}')

        while last_pos.y <= self.screen.get_height():

            # print(f'arrow height: {self.screen_size.y - last_pos.y}')
            # sleep(.1)
            new_pos = last_pos + arrow_vector
            if new_pos.x >= self.screen.get_width():
                break

            if new_pos.y >= self.screen.get_height():
                break

            if new_pos.x >= self.target.position.x:
                break
            # if new_pos.y >= self.target.position.y:
            #     break

            pygame.draw.line(self.screen, color, last_pos.float_list, new_pos.float_list)
            last_pos = new_pos.copy()
            arrow_vector += gravity
            # if counter > 10:
            #     break
            # counter += 1
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

    def volley_Threaded(self):
        self.start()

    def waitForFire(self):
        self.join()
