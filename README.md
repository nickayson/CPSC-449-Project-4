# WordleCPSC449
This is a project for class. An API and database system that can handle requests relating to the game "Wordle".
In this project we created the replicas of the database and distributed reads among them.
We have also created one micoservice to maintain the leaderboard for the wordle games.

## Developed by:      
Nicholas Ayson   
Shivangi Shakya   
Ming Chen


7 PM: Tuesday Class
Section-01         


# Welcome to Project 4

## Set-Up Instructions:

1) Copy the nginx.txt contents into the nginx config file on your system
2) Restart the nginx file with the nginx restart command "sudo service nginx restart"
3) Make var folder with "sh ./bin/start.sh", rq_log folder will also be generated
4) run "foreman start"
5) Inside the directory run "sh ./bin/init.sh" to initiate db
6) The servers should be running after this
7) To have rq enqueue run by cron every 10 mins:  
   1. Run "sh ./bin/rq_cron.sh"
   2. Copy the command that shows in terminal and paste in crontab
   3. Log will be redirected to var/rq_log
   4. If you do not like this way, you can simply add "*/10 * * * * bash -l [directory of rq_enqueue.sh] to crontab
8) For testing the webhook:  
   1. Start the webhook service https://github.com/ProfAvery/cpsc449/tree/master/quart/webhooks by changing the PORT to 6000 in a separate terminal.
   2. In a different terminal, run: ngrok http 6000
9) Open a new terminal and begin making API calls below


## API calls using http:

	Sign-Up:                          http POST tuffix-vm/signup username=[example] password=[example]
	
	Subscribe Webhook:		   http POST http://127.0.0.1:5400/add-leaderboard/

	Make new game:                    http --auth username:password POST tuffix-vm/makeGame

	Get all current games for user:   http --auth username:password GET  http://tuffix-vm/getGames

	Make a guess for a game:          http --auth username:password POST tuffix-vm/makeGuess guess=[apple] game_id=[example]

	Get game status:                  http --auth username:password GET tuffix-vm/gameStatus/[game_id]

	Leaderboard results:              http POST http://127.0.0.1:5400/results/ game_id=[game_id] username=[username] win=[1 or 0] num_guesses=[numofguesses]

	Leaderboard top-scores:           http GET http://127.0.0.1:5400/top-scores/
	
	Add webhook:                      http --auth username:password POST tuffix-vm/add_webhook url=<url>
	
	List all webhooks:                http --auth username:password GET tuffix-vm/getWebhooks

In top-scores we have dummy data with scores of 0 and will get removed as you add more users with higher scores
In leaderboard ensure to Flush the redis database before running Leaderboard commands redis-cli> FLUSHDB



## Online References:
https://dev.to/danielkun/nginx-everything-about-proxypass-2ona
http://nginx.org/en/docs/http/ngx_http_upstream_module.html
https://stackoverflow.com/questions/9523910/iterating-through-a-redis-sorted-set-to-update-an-active-record-table
