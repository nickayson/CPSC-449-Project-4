import collections
import dataclasses
import sqlite3
import textwrap 
import random

import databases
import toml
import uuid
import redis

from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)
        
# Initialize redis client
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

@dataclasses.dataclass
class LeaderboardInfo:
    game_id: str
    username: str
    num_guesses: int
    win: bool
    
# connect to reddis db at port 6379
def get_redis_db():
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r

# Keep track of the score based on if user won the game
def get_score(guesses, win):
    if not win:
        return 0
    elif guesses == 1:
        return 6
    elif guesses == 2:
        return 5
    elif guesses == 3:
        return 4
    elif guesses == 4:
        return 3
    elif guesses == 5:
        return 2
    elif guesses == 6:
        return 1
    else:
        return 0

# Results completely seperated from other services
@app.route("/results/", methods=["POST"])
@validate_request(LeaderboardInfo)
async def score(data: LeaderboardInfo):
    redisdb = get_redis_db()
    game_data = dataclasses.asdict(data)
    
    game_id = game_data["game_id"]
    username = game_data["username"]
    win = game_data["win"]
    num_guesses = game_data["num_guesses"]

    # Set data for a game
    redisdb.hset(game_id, "win", int(win))
    redisdb.hset(game_id, "username", username)
    redisdb.hset(game_id, "num_guesses", num_guesses)

    # Keeps track of the score
    redisdb.hincrby(username, "games")
    current_score = redisdb.hget(username, "score")
    game_score = get_score(num_guesses, win)

    # games for the user
    games = redisdb.hget(username, "games")
    
    if current_score is not None :
        current_score = current_score.decode("utf-8")
    else:
        current_score = 0
    if games is not None:
        games = games.decode("utf-8")
    else:
        games = 1
    
    avg = (int(current_score) + int(game_score)) // int(games)
    redisdb.hset(username, "score", avg)
    
    redisdb.zadd("players", {username: avg})
    
    
    # return format
    leaderboard_info = {
        "game_id": game_id, 
        "username": username, 
        "win": win, 
        "num_of_guesses": num_guesses,
        "score": game_score
    }

    return leaderboard_info
    
# TOP 10 Scores
@app.route("/top-scores/", methods=["GET"])
async def topScores():
    
    redisdb = get_redis_db()
    
    #dummy data
    j=1
    while j<=9:
        test = "dummy" + str(j)
        # all tests have score 0
        redisdb.zadd("players",{test: 0})
        j+=1
        

    arr = redisdb.zrevrange("players", 0, -1, withscores=True)
    top_players = {}
    i = 0
        
    while i < len(arr) and i < 10:
        player = arr[i]
        top_players[i+1] = player[0].decode("utf-8")
        i += 1

    return top_players

# Handle bad routes/errors 
@app.errorhandler(404)
def not_found(e):
    return {"error": "404 The resource could not be found"}, 404

@app.errorhandler(RequestSchemaValidationError) 
def bad_request(e):
    return {"error": str(e.validation_error)}, 400

@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409  

# https://stackoverflow.com/questions/9523910/iterating-through-a-redis-sorted-set-to-update-an-active-record-table