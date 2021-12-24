import torch
import random
import numpy as np
from collections import deque
from all_needed_things import Action



MAX_MEMORY = 100_000
BATCH_SIZE = 1000
Learning_rate = 0.001

class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 # меняет случайность действий
        self.discount_rate = 0
        self.memory = deque(max_lenght = MAX_MEMORY) # при превышении объема удаляет с начала

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_average_score = []
    total_score = 0
    record = 0
    agent = Agent()


if __name__ == '__main__':
    train()