import random #import so that we can randomly add the 2 or 4 tile
import copy # used to create a deep copy of board so can be compared to og
# deep copy copies recursively so og stays unchanged

class Game2048:
    def __init__(self): # self thing is like this-> in C++, can also think of as private member var
        print("Initializing new game object!")  
        self.size = 4
        self.board = [[0]*self.size for _ in range(self.size)] # creates 4x4 board
        self.add_random_tile() #starts with two random tiles
        self.add_random_tile()
        self.score = 0 #tracks score based on merges
        self.won = False

    def reset(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0  # Reset score here
        self.add_random_tile()  # Only one tile added
        self.add_random_tile()
        self.won = False

    def get_state(self): # return current board state
        return {
           "board":self.board,
           "score":self.score,
           "game_over": self.is_game_over(),
           "won": self.won
        }
    
    def add_random_tile(self): # function to make sure new tiles are only added in empty spaces
        empty = [(r,c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if not empty:
           return
        r,c = random.choice(empty) #pick random empty tile
        self.board[r][c] = 2 if random.random() < 0.9 else 4 # enters a 2 90% of the time and a 4 10% of the time
        # because random gets a float from 0 to 1
        if any(2048 in row for row in self.board):
            self.won = True
    
    def compress_and_merge(self, row):
        #compresses and merges a single row + updates score if any two tiles merge
        new_row = [val for val in row if val != 0]
        i = 0
        merged_row = []
        while i < len(new_row):
            # if there is a tile to right exists and it is equal to curr tile
            if i + 1 < len(new_row) and new_row[i] == new_row[i+1]: 
                merged = new_row[i] * 2
                self.score += merged
                merged_row.append(merged)
                i += 2
            else: #if not merged, add same row as merged row & increment i
                merged_row.append(new_row[i])
                i += 1
        
        while len(merged_row) < self.size:
            merged_row.append(0)
        return merged_row
    
    def move_left(self): #create this function for left and intsead of creating one for each direction, just rotate board to be oriented left for each change
        moved = False # create boolean value
        new_board = []
        for row in self.board:
            new_row = self.compress_and_merge(row) #compress and merge each row in the curr board
            if new_row != row: # if something changed
                moved = True # the row  has moved
            new_board.append(new_row) # add each new row to the new board
        if moved:
            self.board = new_board
            #self.add_random_tile() #because something moved, add a new tile to start next "round"

    
    def rotate_clockwise(self):
        self.board = [list(row) for row in zip(*self.board[::-1])]

    def rotate_counterclockwise(self):
        self.board = [list(row) for row in zip(*self.board)][::-1]
    
    def move(self, direction):
        """ 0 = left, 1 = up, 2 = right, 3 = down """ #like a comment but can be accessed in doc file
        backup = copy.deepcopy(self.board)
        if direction == 0: #left
            self.move_left()
        elif direction == 1: # up (rotate, do action, put back)
            self.rotate_counterclockwise()
            self.move_left()
            self.rotate_clockwise()
        elif direction == 2: #right (rotate, do action, put back)
            self.rotate_clockwise()
            self.rotate_clockwise()
            self.move_left()
            self.rotate_counterclockwise()
            self.rotate_counterclockwise()
        elif direction == 3: #down (rotate, do action, put back)
            self.rotate_clockwise()
            self.move_left()
            self.rotate_counterclockwise()
        
        if self.board != backup: #if somethign changed
            self.add_random_tile()
    
    def display(self):
        print(f"Score: {self.score}")
        for row in self.board:
            print(["." if val == 0 else val for val in row])

    def is_game_over(self):
        # Check for any empty tile
        for row in self.board:
            if 0 in row:
                return False

        # Check for any mergeable neighbors
        for r in range(self.size):
            for c in range(self.size):
                if c + 1 < self.size and self.board[r][c] == self.board[r][c + 1]:
                    return False
                if r + 1 < self.size and self.board[r][c] == self.board[r + 1][c]:
                    return False

        return True