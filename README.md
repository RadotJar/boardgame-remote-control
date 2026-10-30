# boardgame-remote-control
A setup to allow a remote friend to play a boardgame as if they were at the table (kinda)

## Make it go

Assuming you already know how to setup python venv, install packages from requirements.txt files (in `server` and `client-laser`)
I have a separate venv for each but you don't need to.

### Run server

`python ./server/server.py`

Will run a uvicorn web server that forwards traffic to socket io server at `localhost:5000`

### Open web client

Open `./client-web/index.html` in browser. Will attempt to make a socket connection to `localhost:5000`. Upon success, status indicator will show green and connected.

Web page will track any key press and log it with `... awaiting ACK`.

### Run laser client

`python ./server/laser.py`

Will run a python socketio client that tries to connect to server at `localhost:5000`. 

Listens for `key_press` events from server (ultimately sent by web clients) and acks them.

With at least one laser client running, web client key presses should be acked, causing the log message on the web client to change to `ACKED by laser`

## Make it go far far away

For this project to actually be useful, you'll want the laser client and web client to be at different network locations. 

Recommended setup:

1. Host the server (`server/server.py`) somewhere
2. Copy the laser client (`server/laser.py`) to the machine that has the physical laser to it. Ensure it has network access
3. Copy the web client (`client-web/index.html`) to the machine you want to connect to the laser from
4. Edit the hardcoded `localhost:5000` network locations in each script to point to the right places
5. Run all the scripts!
6. Leave the magic of the internet to do the rest ( or meddle with the foul powers at your own behest )
