#!/bin/sh

sqlite3 ./var/primary/mount/games.db < share/games.sql

sqlite3 ./var/users.db < share/users.sql

# ./var > mkdir primary secondary third 