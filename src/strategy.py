# check out this article for more info: https://www.geeksforgeeks.org/q-learning-in-python/
import random
import os.path
import pickle

data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data"
strategyx_file = data_dir + "/strategyx.pkl"
strategyo_file = data_dir + "/strategyo.pkl"


class Strategy:
    def __init__(self, gamma, epsilon, alpha):
        self.qdict = {}  # value: qvalue
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # explore factor
        self.alpha = alpha  # learn rate

    def selectAction(self, s, a_space):
        if random.random() < self.epsilon:  # explore
            return random.choice(a_space)
        else:  # find action with highest qvalue in self.qdict
            sdict = {}
            for key, val in self.qdict.items():
                if key[0] == s:
                    sdict[key] = val
            if not sdict:
                return random.choice(a_space)
            else:  # find best action from sdict
                max_qval = list(sdict.values())[0]
                max_a = list(sdict.keys())[0][1]
                for key, val in sdict.items():
                    if val > max_qval:
                        max_qval = value
                        max_a = key[1]
                return max_a

    def update(self, s, sprime, a, r, d):
        if not (s, a) in self.qdict:
            self.qdict[(s, a)] = 0
        if d:  # set qvalue
            self.qdict[(s, a)] = r
        else:  # find all keys containing sprime
            qval_sprime = []
            for key in self.qdict.keys():
                if key[0] == sprime:
                    qval_sprime.append(self.qdict[key])
            max_qval_sprime = 0 if not qval_sprime else max(qval_sprime)
            self.qdict[(s, a)] *= (1 - self.alpha)
            self.qdict[(s, a)] += self.alpha * (r + self.gamma*max_qval_sprime)
