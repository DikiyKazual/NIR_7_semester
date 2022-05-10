import torch
import random
import numpy as np
from collections import deque
from GameForAI import PlatformerForAi
from Model import Linear_QNet, QTrainer
import matplotlib.pyplot as plt
from IPython import display


MAX_MEMORY = 100_000
BATCH_SIZE = 1000  # 1000
Learning_rate = 0.001  #0.001


class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0  # меняет случайность действий
        self.discount_rate = 0.9  # 0.9
        self.memory = deque(maxlen = MAX_MEMORY)  # при превышении объема удаляет с начала
        self.model = Linear_QNet(25, 1024, 5) # 25 входов, 5 выходов  #(, 256, 5)
        self.trainer = QTrainer(self.model, lr=Learning_rate, gamma=self.discount_rate)

    def get_state(self, game):
        x = game.x
        y = game.y
        hp = game.hp
        max_hp = game.max_hp
        need_to_heal = False
        if hp/max_hp < 0.5:
            need_to_heal = True
        facing = True
        facing_center = True
        # куда сейчас движется
        if game.facing == 1:
            facing = True
        elif game.facing == -1:
            facing = False
        in_jump = game.in_jump
        in_fall = game.in_fall
        in_attack = game.in_attack

        distances_to_heal_packs = []
        for i in range(len(game.heal_packs)):
            distance = ((game.heal_packs[i].x - game.x) ** 2 + (game.heal_packs[i].y - game.y) ** 2) ** 0.5
            distances_to_heal_packs.append(distance)
        index_of_closest_heal = np.argmin(distances_to_heal_packs)

        distances_to_enemies = []
        for i in range(len(game.enemies)):
            distance = ((game.enemies[i].x - game.x) ** 2 + (game.enemies[i].y - game.y) ** 2) ** 0.5
            distances_to_enemies.append(distance)
        index_of_closest_enemy = np.argmin(distances_to_enemies)

        if (facing) and (game.x < game.enemies[index_of_closest_enemy].x):
            facing_closest_enemy = True
        elif (not facing) and (game.x > game.enemies[index_of_closest_enemy].x):
            facing_closest_enemy = True
        else:
            facing_closest_enemy = False

        if (game.x <= int(game.winx/2)) and facing:
            facing_center = True
        elif (game.x >= int(game.winx/2)) and (not facing):
            facing_center = True
        else:
            facing_center = False

        state = [
            x,
            y,
            hp,  # Health of a player
            need_to_heal,

            len(game.enemies),

            min(distances_to_heal_packs),  # расстояние до ближайшей лечилки

            min(distances_to_enemies),  # расстояние до ближайшего врага

            facing,  # Move direction
            in_jump,
            in_fall,
            in_attack,
            facing_closest_enemy,
            facing_center,


            game.x > game.enemies[0].x,  # boss to the left
            game.x < game.enemies[0].x,  # boss to the right
            game.y > game.enemies[0].y,  # boss to the up
            game.y < game.enemies[0].y,  # boss to the down

            game.x > game.enemies[index_of_closest_enemy].x,  # closest enemy to the left
            game.x < game.enemies[index_of_closest_enemy].x,  # closest enemy to the right
            game.y > game.enemies[index_of_closest_enemy].y,  # closest enemy to the top
            game.y < game.enemies[index_of_closest_enemy].y,  # closest enemy to the bottom

            game.x > game.heal_packs[index_of_closest_heal].x,  # closest heal to the left
            game.x < game.heal_packs[index_of_closest_heal].x,  # closest heal to the right
            game.y > game.heal_packs[index_of_closest_heal].y,  # closest heal to the top
            game.y < game.heal_packs[index_of_closest_heal].y  # closest heal to the bottom
            ]
        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves
        self.epsilon = 80 - self.number_of_games  # 80
        final_move = [0,0,0,0,0] # right = 0 left = 1 up = 2 down = 3 attack = 4
        if random.randint(0, 200) < self.epsilon:  # (0, 200)
            move = random.randint(0, 4)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

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
        reward, done, score = game.frame_step(final_move)
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


plt.ion()
def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)


if __name__ == '__main__':
    train()