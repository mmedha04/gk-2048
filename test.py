from game2048 import Game2048  # Only needed if using separate file

game = Game2048()

# Manually set up a known board:
game.board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 2, 0, 0]
]
game.score = 0

print("Before move:")
game.display()

game.move(0)  # Move left

print("\nAfter move:")
game.display()