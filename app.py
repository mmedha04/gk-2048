from flask import Flask, render_template, jsonify, request
from game2048 import Game2048

app = Flask(__name__) #flask web application
game = Game2048() # instance of my game

# Route: Home page (GET request to "/")
@app.route("/")
def index():
    return render_template("index.html") #renders(displays) main html page (will show game)

#Route: Get current game state(GET request to "/state")
@app.route("/state")
    # Return the current board and score as JSON
    # Frontend will use this to draw the board
def get_state():
    return jsonify(game.get_state()) #jsonify converts python data into JSON for the front end

#Route: make a move (POST request to "/move")
@app.route("/move", methods=["POST"])
def move():
    #parse the JSON data (make it understandable for the program?)
    data = request.get_json() #retrieve json data
    direction = data.get("direction") #0 = left, 1 = up, 2 = right, 3 = down

    #if direction is valid
    if direction in [0,1,2,3]:
        game.move(direction) # call game logic

    #return updated game state so front end knows what it looks like
    return jsonify(game.get_state())

#Route: Reset the game (POST "/reset")
@app.route("/reset", methods=["POST"])
def reset():
    #Resart the game which means a clear board with 2 empty tiles
    game.reset()
    return jsonify(game.get_state())


# Main runner: starts the development web server
if __name__ == "__main__":
    # Enable live-reload and error messages
    app.run(debug = True)
