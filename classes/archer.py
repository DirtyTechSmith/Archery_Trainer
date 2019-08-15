import math
import tensorflow as tf
import pygame
import random
from time import sleep
from classes.position2d import Position2D

MAX_BOW_STR = 100.0


class ArcherBrain(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.input_2d = tf.keras.layers.Dense(5, activation=tf.nn.sigmoid)
        self.hidden_1 = tf.keras.layers.Dense(1024 , activation=tf.nn.relu)
        self.hidden_2 = tf.keras.layers.Dense(1024, activation=tf.nn.relu)
        self.output_2d = tf.keras.layers.Dense(3, activation=tf.nn.softmax)
    
    def call(self, inputs):
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


class Archer(object):
    def __init__(self, position, screen, screen_size, bow_str=MAX_BOW_STR, brain=None):
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
        gravity = Position2D([0.0, 9.8])
        enemy_position = Position2D(enemy_position)
        inputs = [self.position.x, self.position.y, enemy_position.x, enemy_position.y, self._bow_str]
        results = self.brain.call(inputs)  # type: tf.Tensor
        the_list = [float(thing) for thing in results[0]]
        print(f'bow pullback: {the_list[2]}')
        arrow_speed = (self._bow_str / 2.0) + (the_list[2] * (self._bow_str / 2.0))
        # arrow_speed *= arrow_speed
        arrow_speed = arrow_speed * 3
        print(f'arrow speed: {arrow_speed}')
        arrow_vector = Position2D([the_list[0], (0.0 - the_list[1])])
        print(arrow_vector)
        
        arrow_vector.scalarMultiplication(arrow_speed)
        
        print(arrow_vector)
        
        import random
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        start_pos = self.position
        last_pos = self.position.copy()
        counter = 0
        while (last_pos.y <= self.screen_size.y):
            # print(f'arrow height: {self.screen_size.y - last_pos.y}')
            # sleep(.1)
            new_pos = Position2D.sum(last_pos, arrow_vector)
            if new_pos.x >= self.screen_size.x:
                break
            
            if new_pos.y >= self.screen_size.y:
                break
            
            pygame.draw.line(self.screen, color, last_pos.position_list, new_pos.position_list)
            last_pos = new_pos.copy()
            arrow_vector.increase(gravity)
            # if counter > 10:
            #     break
            # counter += 1
        # end_pos = Position2D.sum(start_pos, arrow_vector)
        miss = Position2D.distance(last_pos, enemy_position)
        print(f'I missed by this much: {miss}')
        # reward =  missToRewardFn(miss)
        # self.Reward(reward)
    # def reward(self, ):
