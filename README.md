# Wordle Backend Project 3

Group 3 team members:
Ming Chen  
Nolan O'Donnell  
Henry Chen

-------------------------------------------------
***Important:   
Test case examples are not provided in the tar. If you want to test endpoints without looking
into the code, refer to the end of this readme.   
Because this code has been modified by a number of people without proper communication,
syntax and naming style are very confusing.In case you have hard time identifying what command
to execute, refer to Sample Test Cases Using httpie part of this readme file or contact me
at mingalexchen@csu.fullerton.edu***
-------------------------------------------------



Steps to run the project:

0. Prepare your own litefs, and copy it to bin folder.
   Litefs is not provided in bin folder of this tar.

Note: if you use code downloaded from this repo, you need to add
      mount & data directory manually.
      To avoid this, use the tar provided in this repo.

1. Copy the nginx configuration file to sites-enabled by running:

   sudo cp etc/tutorial.txt /etc/nginx/sites-enabled/tutorial

   Note:remember to reload nginx.

2. Start the API by running

   foreman start

3. Initialize the database and start the API:

   sh ./bin/init.sh

4. Populate the data base by running the python script:

   python3 dbpop.py

Note: populating DB before starting services will cause
      mount to fail.      


5. Using http://tuffix-vm should yield in redirecting requests
   over to provided appropriate microservices.

   You may refer to /etc/tutorial.txt to find all provided
   redirection for tuffix-vm.

   location of each service as local ip
   game1,2,3:   
   http://127.0.0.1:5200   
   http://127.0.0.1:5400   
   http://127.0.0.1:5600   

   user:  
   http://127.0.0.1:5000

   Note: as auth is set to be internal, accessing it with
         tuffix-vm server name will return error code.
         It works correctly as a pop up.

   leaderboard:
   http://127.0.0.1:5700

   Note: nosql DB is NOT populated by default.
   To populate it, access the /add-score/ endpoint or
   http://127.0.0.1:5700/scores/ to add scores to it.


Files to turn in:

1. Python source code:

   game.py  
   user.py  
   leaderboard.py

2. Procfile:

   Procfile contains 3 microservices game, leaderboard and
   user that have no coupling. It also contains

3. Initialization and population scripts for the databases:

   dbpop.py - populates the database with wordle words  
   game.sql - contains database for game microservice  
   user.sql - contains database for user microservice  
   init.sh - Initializes the databases to be created  

4. Nginx configuration files:

   tutorial.txt

5. Any other necessary configuration files:

   correct.json  
   valid.json - both populate the database with dbpop.py file  
   game.toml  
   user.toml - allows the source to connect to the database
   primary.yml
   secondary.yml
   secondary2.yml- configuration files for litefs

# Sample Test Cases Using httpie:

- registering an new account   
  command:   
    http post http://127.0.0.1:5000/users/ "first_name=alex" "last_name=chen" "user_name=Alex" "password=449"

sample result
![image](/endpoint_demo/game_register_1.png)

  Use this account for auth afterwards.

  If you wish to access this endpoint as tuffix-vm/register/ without having to
  use auth, remove

	location / {
		#login popup
		auth_request /auth;
		auth_request_set $auth_status $upstream_status;
  	}

  In tutorial.txt, and update nginx config again.

   The command would now be   
   http post http://tuffix-vm/register/ "first_name=alex" "last_name=chen" "user_name=Alexc" "password=449"

Sample result
![image](/endpoint_demo/game_register_2.png)


- post a score to redis   
  command:   
  http post http://tuffix-vm/add-score/ "user"="Alex clone1" "score"="1"

sample result
![image](/endpoint_demo/leaderboard_post_score.png)

### note: redis is not pre-populated. You need to add content into it yourself


- retrive top ten score   
  command:   
  http get http://tuffix-vm/top-ten/

sample result
![image](/endpoint_demo/leaderboard_topten.png)

- start a new game   
  command:   
  http post http://Alex:449@tuffix-vm/new-game/

sample result  
![image](/endpoint_demo/game_newgame.png)

we can see that data is then being backuped in replica dbs
  ![image](/endpoint_demo/game_newgame_dbreplica.png)

- make a move    
  command:   
  http post http://Alex:449@tuffix-vm/game-guess/ "gameid"="7b4f3128-1449-4d52-b569-2a521c2be0e9" "word"="clomp"

  Note: you will need to use an id that exist in your db to make a move.
  Using this command directly is very unlikely to give the same result.

  sample result:
![image](/endpoint_demo/game_make_a_move.png)

  Note2: original contributor of this project did not implement valid and
  correct word in the way it should be. API never checks if guess is a correct
  word and only checks if guess is the answer or if guess is a valid word.
  You may check this in game.py line 213-263.
  Due to the purpose of this project and time constrain, I did not try to
  fix this issue in afraid of causing more bugs that are hard to fix.

- retrive in progress games   
  command:   
  http get http://Alex:449@tuffix-vm/get-user-games/

  sample result:
  ![image](/endpoint_demo/game_user_allgame.png)

- get game status by id   
  command:   
  http get http://Alex:449@tuffix-vm/grab-game-by-id/7b4f3128-1449-4d52-b569-2a521c2be0e9

  sample result:
  ![image](/endpoint_demo/game_game_by_id.png)


  Note:   
  Read replica is done by maintaining connections to three dbs and
  communicate to a db selected by cycle.next.  

    DB connection and teardown:  
  ![image](/endpoint_demo/read_replica_conne.png)  


  sample DB selection:  
  ![image](/endpoint_demo/read_replica_select.png)
