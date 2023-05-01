#!/bin/sh

gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker --bind 0.0.0.0:5000 server:app &
sudo -u ggeasy autossh -M 0 -o serverAliveInterval=60 -R tictactoegame.serveo.net:80:0.0.0.0:5000 serveo.net