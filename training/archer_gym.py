from random import randint
from typing import Tuple, Dict, Any

import gym
import numpy as np
import pygame

from classes.archer import Archer, ArcherBrain
from classes.entity import Entity
from vector import Vector


class Enemy(Entity):
    """
    An enemy class for the archer to target.
    """

    def __init__(self, position, screen):
        super().__init__(position, screen)


class TrainArchers(gym.Env):
    """
    A custom Gym environment for training an archer.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(TrainArchers, self).__init__()
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)
        self._screen: pygame.Surface = pygame.display.set_mode([800, 600])
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._archer: Archer = Archer(Vector([400, 300]), self._screen, target=self.create_enemy(), brain=ArcherBrain())
        self._archer.start()
        self._done: bool = False
        self._reward: int = 0
        self._info: Dict[str, Any] = {}

        # Create an enemy with a random position on the right half of the screen
        enemy_x = randint(self._screen.get_width() // 2, self._screen.get_width())
        enemy_y = randint(0, self._screen.get_height())
        self._enemy: Enemy = Enemy(Vector([enemy_x, enemy_y]), self._screen)

    def create_enemy(self, pos: Vector = None) -> Enemy:
        if pos is None:
            enemy_x = randint(self._screen.get_width() // 2, self._screen.get_width())
            enemy_y = randint(0, self._screen.get_height())
            pos = Vector([enemy_x, enemy_y])

        enemy = Enemy(pos, self._screen)
        return enemy

    def step(self, action: int) -> Tuple[np.ndarray, int, bool, Dict[str, Any]]:
        self._archer.step(action)
        self._archer.wait()
        self._archer.start()
        self._reward = self._archer.reward
        self._done = self._archer.done
        self._info = self._archer.info
        return self._archer.observation, self._reward, self._done, self._info

    def reset(self) -> np.ndarray:
        self._archer.reset()
        return self._archer.observation

    def render(self, mode: str = 'human', close: bool = False) -> None:
        self._clock.tick(60)
        self._screen.fill((0, 0, 0))
        self._archer.render()
        self._enemy.render()  # Render the enemy
        pygame.display.flip()

    def close(self) -> None:
        pygame.quit()

    def seed(self, seed: Any = None) -> None:
        pass

    def __del__(self) -> None:
        pygame.quit()


if __name__ == '__main__':
    env = TrainArchers()
    for i_episode in range(20):
        observation = env.reset()
        for t in range(100):
            env.render()
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            if done:
                print("Episode finished after {} timesteps".format(t + 1))
                break
    env.close()
