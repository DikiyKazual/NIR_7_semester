import torch
import random
import numpy as np
from collections import deque
from all_needed_things import Action, balls_collide as b_k
from GameForAI import PlatformerForAi



MAX_MEMORY = 100_000
BATCH_SIZE = 1000
Learning_rate = 0.001

class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 # меняет случайность действий
        self.discount_rate = 0
        self.memory = deque(max_lenght = MAX_MEMORY) # при превышении объема удаляет с начала
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        #position = [game.x, game.y]
        #point_to_left = [game.x - game.radius - game.speed, game.y]
        #point_to_right = [game.x + game.radius + game.speed, game.y]
        #point_to_bottom = [game.x, game.y + 2 * game.radius]
        #point_to_top = [game.x, game.y - 2 * game.radius]

        # куда сейчас движется
        dir_up = game.in_jump
        dir_down = game.in_fall
        dir_attack = game.in_attack

        danger_to_the_left = False
        danger_to_the_right = False
        danger_to_the_up = False
        danger_to_the_down = False

        for enemy in game.enemies:
            if (b_k((game.x - game.radius - game.speed, game.y, game.radius),
                    (enemy.x, enemy.y + int(enemy.radius * 0.1), int(enemy.radius * 0.95))) or (
                        b_k((game.x - game.radius - game.speed, game.y - game.radius, game.radius), (enemy.x, enemy.y,
                                                                          int(enemy.radius * 0.9))))):
                danger_to_the_left = True
        for enemy in game.enemies:
            if (b_k((game.x + game.radius + game.speed, game.y, game.radius),
                    (enemy.x, enemy.y + int(enemy.radius * 0.1), int(enemy.radius * 0.95))) or (
                        b_k((game.x + game.radius + game.speed, game.y - game.radius, game.radius), (enemy.x, enemy.y,
                                                                          int(enemy.radius * 0.9))))):
                danger_to_the_right = True
        for enemy in game.enemies:
            if (b_k((game.x, game.y - 2 * game.radius, game.radius),
                    (enemy.x, enemy.y + int(enemy.radius * 0.1), int(enemy.radius * 0.95))) or (
                        b_k((game.x, game.y - 3 * game.radius, game.radius), (enemy.x, enemy.y,
                                                                          int(enemy.radius * 0.9))))):
                danger_to_the_up = True
        for enemy in game.enemies:
            if (b_k((game.x, game.y + 2 * game.radius, game.radius),
                    (enemy.x, enemy.y + int(enemy.radius * 0.1), int(enemy.radius * 0.95))) or (
                        b_k((game.x, game.y + game.radius, game.radius), (enemy.x, enemy.y,
                                                                          int(enemy.radius * 0.9))))):
                danger_to_the_down = True




        state = [
            # Danger left
            danger_to_the_left,

            # Danger right
            danger_to_the_right,

            # Danger up
            danger_to_the_up,

            # Danger down
            danger_to_the_down,

            # Move direction
            dir_up,
            dir_down,
            dir_attack,

            # Boss location
            game.x > game.enemies[0].x, # boss to the left
            game.x < game.enemies[0].x, # boss to the right
            game.y > game.enemies[0].y,  # boss to the up
            game.y < game.enemies[0].y  # boss to the down
            ]

        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_average_score = []
    total_score = 0
    record = 0
    agent = Agent()
    game = PlatformerForAi()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get action
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset_game()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.number_of_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_average_score.append(mean_score)
            plot(plot_scores, plot_average_score)


if __name__ == '__main__':
    train()