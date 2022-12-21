import gym
import pygame

from classes.archer import Archer, ArcherBrain
from vector import Vector

"A gym environment named TrainArchers, with a 2d unit that has a training step, and resets the pygame environment"


class TrainArchers(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(TrainArchers, self).__init__()
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(5,), dtype=np.float32)
        self._screen = pygame.display.set_mode([800, 600])
        self._clock = pygame.time.Clock()
        self._archer = Archer(Vector(400, 300), self._screen, None, brain=ArcherBrain())
        self._archer.start()
        self._done = False
        self._reward = 0
        self._info = {}

    def step(self, action):
        self._archer.step(action)
        self._archer.wait()
        self._archer.start()
        self._reward = self._archer.reward
        self._done = self._archer.done
        self._info = self._archer.info
        return self._archer.observation, self._reward, self._done, self._info

    def reset(self):
        self._archer.reset()
        return self._archer.observation

    def render(self, mode='human', close=False):
        self._clock.tick(60)
        self._screen.fill((0, 0, 0))
        self._archer.render()
        pygame.display.flip()

    def close(self):
        pygame.quit()

    def seed(self, seed=None):
        pass

    def __del__(self):
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
