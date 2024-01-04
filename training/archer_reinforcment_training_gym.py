from random import randint

import gym
import numpy as np
import pygame

from classes.archer import Archer, ArcherBrain
from classes.entity import Entity
from vector import Vector


class ArcherTrainingEnv(gym.Env):
    """
    A custom Gym environment for training an Archer's neural network.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(ArcherTrainingEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)
        self._screen: pygame.Surface = pygame.display.set_mode([800, 600])
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._archer: Archer = Archer(Vector([400, 300]), self._screen, target=self.create_enemy(), brain=ArcherBrain())
        self._archer.start()
        self._done: bool = False
        self._reward: int = 0
        self._info: dict[str, any] = {}

    def create_enemy(self, pos: Vector = None) -> Entity:
        if pos is None:
            enemy_x = randint(self._screen.get_width() // 2, self._screen.get_width())
            enemy_y = randint(0, self._screen.get_height())
            pos = Vector([enemy_x, enemy_y])

        enemy = Entity(pos, self._screen)
        return enemy

    def step(self, action: int) -> tuple[np.ndarray, int, bool, dict[str, any]]:
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
        pygame.display.flip()

    def close(self) -> None:
        pygame.quit()

    def seed(self, seed = None) -> None:
        pass

    def __del__(self) -> None:
        pygame.quit()


if __name__ == '__main__':
    env = ArcherTrainingEnv()
    # Here you can use a reinforcement learning algorithm to train the ArcherBrain neural network.
    # For example, you can use algorithms from stable-baselines3 library.
    # model = PPO('MlpPolicy', env, verbose=1)
    # model.learn(total_timesteps=10000)
    # obs = env.reset()
    # for i in range(1000):
    #     action, _states = model.predict(obs, deterministic=True)
    #     obs, reward, done, info = env.step(action)
    #     env.render()
    #     if done:
    #         obs = env.reset()
    env.close()
