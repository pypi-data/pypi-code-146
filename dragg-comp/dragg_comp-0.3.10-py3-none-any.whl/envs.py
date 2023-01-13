from datetime import datetime
import asyncio
import argparse

from dragg_comp.player import PlayerHome
# from submission.submission import *

REDIS_URL = "redis://localhost"

class RLTrainingEnv(PlayerHome):
	def __init__(self, redis_url=REDIS_URL, normalization=None, reward=None):
		self.normalization = normalization
		self.reward = reward
		super().__init__(redis_url=redis_url)
		
	def get_reward(self):
		# redefines get_reward with the player's implementation
		return self.reward(self)

	def reset(self, initialize=False):
		super().reset()
		return self.normalization(self)

	def step(self, action):
		obs = super().step(action)
		reward = self.get_reward()
		return self.normalization(self), reward, False, {}