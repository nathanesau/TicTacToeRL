import random
import os.path
import pickle

data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data"
strategyx_file = data_dir + "/strategyx.pkl"
strategyo_file = data_dir + "/strategyo.pkl"

# qlearning logic
class Strategy:
    def __init__(self, discount_factor, explore_factor, learn_rate):
        self.qtable = {} # key: tuple(tuple(board.data), action_index), value: qvalue
        self.discount_factor = discount_factor
        self.explore_factor = explore_factor
        self.learn_rate = learn_rate

    def selectAction(self, curr_state, action_space):
        r = random.random() # between 0 and 1
        if r < self.explore_factor: # explore
            return random.choice(action_space)
        else: # find action with highest qvalue in self.qtable
            curr_state_dict = {}
            for key, value in self.qtable.items():
                if key[0] == curr_state:
                    curr_state_dict[key] = value
            if len(curr_state_dict) == 0:
                return random.choice(action_space)
            else: # find best action from curr_state_dict
                max_qvalue = list(curr_state_dict.values())[0]
                max_action = list(curr_state_dict.keys())[0][1]
                for key, value in curr_state_dict.items():
                    if value > max_qvalue:
                        max_qvalue = value
                        max_action = key[1]
                return max_action

    # curr_state: current board.data
    # next_state: next board.data
    # done: true if game is over, false otherwise
    def update(self, curr_state, next_state, action, reward, done):
        curr_key = (curr_state, action)
        key_exist = (curr_state, action) in self.qtable
        if not key_exist:
            self.qtable[curr_key] = 0
        if done:
            self.qtable[curr_key] = reward
        else: # find all keys containing next_state
            qvalues_next_state = []
            for key in self.qtable.keys():
                if key[0] == next_state:
                    qvalues_next_state.append(self.qtable[key])
            max_qvalue_next_state = 0 if len(qvalues_next_state) == 0 else max(qvalues_next_state)
            self.qtable[curr_key] = self.qtable[curr_key] * (1 - self.learn_rate) + \
                self.learn_rate * (reward + self.discount_factor * max_qvalue_next_state)
