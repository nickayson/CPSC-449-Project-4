users_service: hypercorn users_service --reload --debug --bind users_service.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG

primary: ./bin/litefs -config ./etc/primary.yml
secondary: ./bin/litefs -config ./etc/secondary.yml
third: ./bin/litefs -config ./etc/third.yml

leaderboard_service: hypercorn leaderboard_service --reload --debug --bind leaderboard_service.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG

# game_service1: hypercorn game_service --reload --debug --bind game_service.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
# game_service2: hypercorn game_service --reload --debug --bind game_service.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
# game_service3: hypercorn game_service --reload --debug --bind game_service.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG

