import collections
import dataclasses
import sqlite3
import textwrap 
import random

import databases
import toml
import uuid
import redis, ast
import os, socket, httpx, json, requests
from game_service import Webhook

from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)
        
# Initialize redis client
redisClient = redis.Redis("localhost", 6379)

@dataclasses.dataclass
class LeaderboardInfo:
    game_id: str
    username: str
    num_guesses: int
    win: bool
    
# connect to reddis db at port 6379
def get_redis_db():
    r = redis.Redis(host='localhost', port=6379, db=0)
    #r.flushdb()
    return r

def hostname():
	port = os.environ["PORT"]
	domain = socket.getfqdn("127.0.0.1")
	host = "http://"+domain+":"+port+"/results/"
	return host

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

@app.route("/add-leaderboard/", methods=["POST"])
async def add_leaderboard():
	response = httpx.post("http://tuffix-vm/add_webhook", json={"url":str(hostname())})
	return response.text

# Results completely seperated from other services
@app.route("/results/", methods=["POST"])
@validate_request(LeaderboardInfo)
async def score(data: LeaderboardInfo):
	redisdb = get_redis_db()
	game_data = dataclasses.asdict(data)
    
	game_id = game_data["game_id"]
	username = game_data["username"]
	win = game_data["win"]
	num_guesses = int(game_data["num_guesses"])
	
	try:
		score = get_score(num_guesses, win)
		games = 1
		if redisdb.exists(username):
			score_data = ast.literal_eval((redisdb.get(username)).decode("UTF-8"))
			games = int(score_data["games"])
			score = (score + (int(score_data["score"])*games)) / (games + 1)
		res = {
			username: str({
				"score": score,
				"games": games + 1
			})
		}
		data_added = redisdb.mset(res)

		redisdb.zadd("players", {username: score})
			
		if data_added:
			leaderboard_info = {
			"game_id": game_id, 
			"username": username, 
			"win": win, 
			"num_of_guesses": num_guesses,
			"score": score
			}

			return leaderboard_info
		else:
			return {
    					"msg" : "No score added"
    				}
	except:
			return {
				"error": "Game score is submitted.",
				"fix": "Create a new game."
    			}
			
    
# TOP 10 Scores
@app.route("/top-scores/", methods=["GET"])
async def topScores():
    r = get_redis_db()
    arr = r.zrevrange("players", 0, -1, withscores=True)
    top_players = {}
    i = 0
    while i < len(arr) and i < 10:
        player = arr[i]
        top_players[i+1] = player[0].decode("utf-8") + " - " + str(player[1])
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
