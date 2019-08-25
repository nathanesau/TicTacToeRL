import random
import pickle
import os.path

# pickle.dump(strategy1.qtable, open('strategy1.pkl', 'wb'))
# strategy1.qtable = pickle.load(open('strategy1.pkl', 'rb'))

# constants
ID_UNDEFINED = 0
ID_X = 1
ID_O = 2

# for cpu logic
DISCOUNT_FACTOR1 = 0.9
EXPLORE_FACTOR1 = 0.1
LEARN_RATE1 = 0.1

DISCOUNT_FACTOR2 = 0.9
EXPLORE_FACTOR2 = 0.1
LEARN_RATE2 = 0.1

class Board:
    def __init__(self):
        self.data = [[0, 0, 0],[0, 0, 0], [0, 0, 0]]
        self.round = 0

    def getValidMoves(self, id):
        valid_moves = []
        for row in range(3):
            for col in range(3):
                if self.data[row][col] == ID_UNDEFINED:
                    valid_moves.append((row, col))
        return valid_moves

    def updateBoard(self, id, move):
        self.data[move[0]][move[1]] = id
        self.round += 1

    def getWinner(self):
        for id in [ID_X, ID_O]:
            for i in range(3):
                # check rows
                if self.data[i][0] == id and self.data[i][1] == id and self.data[i][2] == id:
                    return id
                # check cols
                if self.data[0][i] == id and self.data[1][i] == id and self.data[2][i] == id:
                    return id
            # check diag
            if self.data[0][0] == id and self.data[1][1] == id and self.data[2][2] == id:
                return id
            if self.data[0][2] == id and self.data[1][1] == id and self.data[2][0] == id:
                return id
        return ID_UNDEFINED
                

    def isBoardFull(self):
        for row in self.data:
            for e in row:
                if e == ID_UNDEFINED:
                    return False
        return True 

    def isGameOver(self):
        return self.getWinner() != ID_UNDEFINED or self.isBoardFull()

    def __str__(self):
        s = ""
        for i in range(3):
            for j in range(3):
                s += str(self.data[i][j])
                if j != 2:
                    s += " "
            if i  != 2:
                s += "\n"
        return s

class Cpu:
    def __init__(self, id):
        self.id = id

    def getMove(self, board):
        validMoves = board.getValidMoves(self.id)
        return validMoves[0] # always choose move[0] (bad)

class Strategy:
    def __init__(self, discount_factor = 0.9, explore_factor = 0.1, learn_rate = 0.1):
        self.qtable = {} # key: tuple(tuple(board.data), action_index), value: qvalue
        self.discount_factor = discount_factor
        self.explore_factor = explore_factor
        self.learn_rate = learn_rate

    # done
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

def getRowInput():
    while True:
        row = input("Enter a row (1, 2, 3): ")
        try:
            row = int(row)
            if row in [1, 2, 3]:
                return row
            else:
                print("invalid input, not in [1,2,3]")
        except:
            print("invalid input, not an integer")

def getColInput():
    while True:
        col = input("Enter a col (1, 2, 3): ")
        try:
            col = int(col)
            if col in [1, 2, 3]:
                return col
            else:
                print("invalid input, not in [1,2,3]")
        except:
            print("invalid input, not an integer")

def getPlayAgain():
    while True:
        playAgain = input("do you want to play again (yes: 1, no : 0): ")
        if int(playAgain) in [1, 0]:
            return playAgain
            print("invalid input, not in [1, 0]")

def playInteractiveGame(strategy1): # done multiple times
    board = Board()
    cpu_id = ID_X
    player_id = ID_O
    curr_id = ID_X

    while not board.isGameOver():
        print(board)

        if curr_id == cpu_id:
            curr_state1 = tuple(tuple(row) for row in board.data)
            action_space1 = board.getValidMoves(ID_X)
            action1 = strategy1.selectAction(curr_state1, action_space1)
            board.updateBoard(cpu_id, action1)
            print("cpu made move: ", action1, "\n")

            if board.isGameOver(): # o doesn't get to go again (they have lost) - update x
                next_state1 = tuple(tuple(row) for row in board.data)
                reward1 = 100 if board.getWinner() is ID_X else 0 if board.getWinner() is ID_UNDEFINED else -100
                strategy1.update(curr_state1, next_state1, action1, reward1, True)
                break

        else: # human
            row = getRowInput()
            col = getColInput()
            action = (row, col)
            board.updateBoard(player_id, (row - 1, col - 1))
            print("human made move: ", action, "\n")

            # update x after o goes
            next_state1 = tuple(tuple(row) for row in board.data)
            reward1 = 100 if board.getWinner() is ID_X else 0 if board.getWinner() is ID_UNDEFINED else -100
            strategy1.update(curr_state1, next_state1, action1, reward1, board.isGameOver())

            if board.isGameOver(): # no strategy2 update necessary
                break
        
        # at end of loop
        curr_id = ID_O if curr_id is ID_X else ID_X

    print("game over: final board...\n")
    print(board)
    winner = board.getWinner()
    winnerStr = "cpu" if winner is cpu_id else "human" if winner is player_id else "none"
    print("winner: ", winnerStr)


def playTrainingGame(strategy1, strategy2): # done multiple times
    board = Board()
    curr_state1, next_state1 = None, None
    curr_state2, next_state2 = None, None
    curr_id = ID_X

    while True:
        
        if curr_id == ID_X:
            curr_state1 = tuple(tuple(row) for row in board.data)
            action_space1 = board.getValidMoves(ID_X)
            action1 = strategy1.selectAction(curr_state1, action_space1)
            board.updateBoard(ID_X, action1)

            # update o after x goes
            if board.round > 1:
                next_state2 = tuple(tuple(row) for row in board.data)
                reward2 = 100 if board.getWinner() is ID_O else 0 if board.getWinner() is ID_UNDEFINED else -100
                strategy2.update(curr_state2, next_state2, action2, reward2, board.isGameOver())

            if board.isGameOver(): # o doesn't get to go again (they have lost) - update x
                next_state1 = tuple(tuple(row) for row in board.data)
                reward1 = 100 if board.getWinner() is ID_X else 0 if board.getWinner() is ID_UNDEFINED else -100
                strategy1.update(curr_state1, next_state1, action1, reward1, True)
                return

        else: # ID_O
            curr_state2 = tuple(tuple(row) for row in board.data)
            action_space2 = board.getValidMoves(ID_O)
            action2 = strategy2.selectAction(curr_state2, action_space2)
            board.updateBoard(ID_O, action2)

            # update x after o goes
            next_state1 = tuple(tuple(row) for row in board.data)
            reward1 = 100 if board.getWinner() is ID_X else 0 if board.getWinner() is ID_UNDEFINED else -100
            strategy1.update(curr_state1, next_state1, action1, reward1, board.isGameOver())

            if board.isGameOver(): # x doesn't get to go again (they have lost) - update o
                next_state2 = tuple(tuple(row) for row in board.data)
                reward2 = 100 if board.getWinner() is ID_O else 0 if board.getWinner() is ID_UNDEFINED else -100
                strategy2.update(curr_state2, next_state2, action2, reward2, True)
                return

        # at end of loop
        curr_id = ID_O if curr_id is ID_X else ID_X

def trainComputer(numGames):
    strategy1 = Strategy(DISCOUNT_FACTOR1, EXPLORE_FACTOR1, LEARN_RATE1) # tune strategy 1
    strategy2 = Strategy(DISCOUNT_FACTOR2, EXPLORE_FACTOR2, LEARN_RATE2) # dumb compute

    if os.path.exists('strategy1.pkl'):
        strategy1.qtable = pickle.load(open('strategy1.pkl', 'rb'))
    if os.path.exists('strategy2.pkl'):
        strategy2.qtable = pickle.load(open('strategy2.pkl', 'rb'))

    for i in range(numGames):
        playTrainingGame(strategy1, strategy2)
    
    # pickle save the qtables
    pickle.dump(strategy1.qtable, open('strategy1.pkl', 'wb'))
    pickle.dump(strategy2.qtable, open('strategy2.pkl', 'wb'))

def playComputer(numGames):
    
    strategy1 = Strategy(DISCOUNT_FACTOR1, 0, LEARN_RATE1) # no update, no explore
    strategy1.qtable = pickle.load(open('strategy1.pkl', 'rb'))

    for i in range(numGames):
        playInteractiveGame(strategy1)

        playAgain = getPlayAgain()
        if not playAgain:
            return

    pickle.dump(strategy1.qtable, open('strategy1.pkl', 'wb'))

if __name__ == "__main__":

    train = False

    if train:
        trainComputer(10000)
    else:
        playComputer(5)
