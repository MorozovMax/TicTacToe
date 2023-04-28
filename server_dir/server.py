"""Server for online game."""

import uuid
import os
import threading
import time
import hashlib
import random
from datetime import timedelta
from typing import Optional, List, Dict, Union
import flask
import jwt
from flask import Flask, request, jsonify, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room, leave_room


app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')

db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database'))

try:
    os.mkdir(db_dir)
except FileExistsError:
    pass

db_path = os.path.join(db_dir, 'game.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'TicTacToe_multiplayer_online_game'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=999999999)

db = SQLAlchemy(app)


class User(db.Model):
    """User class for use in SQLAlchemy."""

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    online_stats = db.relationship('OnlineGameStat', backref='user', lazy=True)
    computer_stats = db.relationship('ComputerGameStat', backref='user', lazy=True)


class ComputerGameStat(db.Model):
    """Computer game statistics class for use in SQLAlchemy."""

    id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False, primary_key=True)
    games_played = db.Column(db.Integer, default=0, nullable=False)
    games_won = db.Column(db.Integer, default=0, nullable=False)
    games_draws = db.Column(db.Integer, default=0, nullable=False)
    games_defeat = db.Column(db.Integer, default=0, nullable=False)


class OnlineGameStat(db.Model):
    """Online game statistics class for use in SQLAlchemy."""

    id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False, primary_key=True)
    games_played = db.Column(db.Integer, default=0, nullable=False)
    games_won = db.Column(db.Integer, default=0, nullable=False)
    games_draws = db.Column(db.Integer, default=0, nullable=False)
    games_defeat = db.Column(db.Integer, default=0, nullable=False)


def hash_password(password: str) -> str:
    """
    Hash password.

    :param password: User password
    :type password: class `str`
    :return: Hashed password
    :rtype: class: `str`
    """
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username: str, password: str) -> str:
    """
    Create a user profile.

    :param username: User username
    :type username: class: `str`
    :param password: User password
    :type password: class `str`
    :return: Id of user
    :rtype: class: `str`
    """
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise ValueError('Username already exists')

    user_id = str(uuid.uuid4())
    hashed_password = hash_password(password)
    user = User(id=user_id, username=username, password=hashed_password)
    computer_stat = ComputerGameStat(id=user_id, games_played=0, games_won=0, games_draws=0, games_defeat=0)
    online_stat = OnlineGameStat(id=user_id, games_played=0, games_won=0, games_draws=0, games_defeat=0)
    db.session.add(user)
    db.session.add(computer_stat)
    db.session.add(online_stat)
    db.session.commit()
    return user_id


def authenticate_user(username: str, password: str) -> Optional[str]:
    """
    Verify the existence of a user.

    :param username: User username
    :type username: class: `str`
    :param password: User password
    :type password: class `str`
    :return: Id of user or None
    :rtype: class: `str` or None
    """
    hashed_password = hash_password(password)
    user = User.query.filter_by(username=username, password=hashed_password).first()
    if user:
        return user.id
    else:
        return None


games: Dict[str, Dict[str, Dict[str, str]]] = {}
users_dict: Dict[str, str] = {}
waiting_players: List[Dict[str, str]] = []
sessions: List[str] = []


def start_game() -> None:
    """Select two players in a separate thread to start the game."""
    while True:
        length = len(waiting_players)

        flag = False

        for i in range(length):
            player1 = waiting_players[i]

            player1_sign = player1['sign']
            player1_turn = player1['turn']

            for j in range(length):
                if i != j:
                    if waiting_players[j]['sign'] != player1_sign and waiting_players[j]['turn'] != player1_turn:
                        flag = True
                        break

            if flag:
                break

        if flag:
            if j > i:
                player2 = waiting_players.pop(j)
                player1 = waiting_players.pop(i)
            elif i > j:
                player1 = waiting_players.pop(i)
                player2 = waiting_players.pop(j)

            game_id = str(uuid.uuid4())

            if player1['turn'] == '1':
                games[game_id] = {'player1': {'id': player1['user_id'], 'sign': player1['sign']},
                                  'player2': {'id': player2['user_id'], 'sign': player2['sign']}}
            else:
                games[game_id] = {'player1': {'id': player2['user_id'], 'sign': player2['sign']},
                                  'player2': {'id': player1['user_id'], 'sign': player1['sign']}}

        time.sleep(5)


t: threading.Thread = threading.Thread(target=start_game, daemon=True)
t.start()


@app.route('/login', methods=['POST'])
def login() -> flask.Response:
    """
    Authorize the user in the game.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    data = request.get_json()
    username = data['username']
    password = data['password']

    user_id = authenticate_user(username, password)

    if user_id:
        if user_id in sessions:
            return jsonify({'message': 'Error'})

        session['user_id'] = user_id
        sessions.append(user_id)
        token = jwt.encode({'user_id': user_id}, app.secret_key, algorithm='HS256')
        pc_stat = ComputerGameStat.query.filter_by(id=user_id).first()
        friend_stat = OnlineGameStat.query.filter_by(id=user_id).first()
        response = make_response(jsonify({'message': 'Login successful', 'user_id': user_id,
                                          'pc_stat': {"drawn_game": pc_stat.games_draws,
                                                      "Player_win": pc_stat.games_won,
                                                      "Computer_win": pc_stat.games_defeat},
                                          'friend_stat': {"drawn_game": friend_stat.games_draws,
                                                          "Player1_win": friend_stat.games_won,
                                                          "Player2_win": friend_stat.games_defeat}
                                          }))
        response.set_cookie('token', token, httponly=True, samesite='Strict')
        return response
    else:
        return jsonify({'message': 'Invalid username or password'})


@app.route('/logout', methods=['GET'])
def logout() -> flask.Response:
    """
    Log the user out of the game.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    sessions.remove(session['user_id'])
    session.pop('user_id', None)
    response = make_response(jsonify({'message': 'Logout successful'}))
    response.delete_cookie('token')
    return response


@app.route('/', methods=['GET'])
def index() -> flask.Response:
    """
    Send the necessary data to the user when launching the client with the game.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    print("yes")
    data = jwt.decode(request.cookies['token'], app.secret_key, algorithms=['HS256'])
    session['user_id'] = data['user_id']
    user = User.query.filter_by(id=data['user_id']).first()
    username = user.username
    pc_stat = ComputerGameStat.query.filter_by(id=data['user_id']).first()
    friend_stat = OnlineGameStat.query.filter_by(id=data['user_id']).first()

    return jsonify({'message': 'Success', 'user': username,
                    'pc_stat': {"drawn_game": pc_stat.games_draws, "Player_win": pc_stat.games_won,
                                "Computer_win": pc_stat.games_defeat},
                    'friend_stat': {"drawn_game": friend_stat.games_draws, "Player1_win": friend_stat.games_won,
                                    "Player2_win": friend_stat.games_defeat}})


@app.route('/register', methods=['POST'])
def register() -> flask.Response:
    """
    Register a user.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        user_id = create_user(username, password)
        return jsonify({'message': 'User created successfully', 'user_id': user_id})
    except ValueError:
        return jsonify({'message': 'Username already exists'})


@app.route('/update_computer_statistic', methods=['POST'])
def update_computer_statistic() -> flask.Response:
    """
    Update statistics of computer games of user.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    token = jwt.decode(request.cookies['token'], app.secret_key, algorithms=['HS256'])
    user_id = token['user_id']
    data = request.get_json()
    games_played = data['games_played']
    games_won = data['games_won']
    games_draws = data['games_draws']
    games_defeat = data['games_defeat']

    user = ComputerGameStat.query.filter_by(id=user_id).first()

    user.games_played = games_played
    user.games_won = games_won
    user.games_draws = games_draws
    user.games_defeat = games_defeat

    db.session.commit()

    return jsonify({'message': 'Game statistics updated successfully'})


@app.route('/update_friend_statistic', methods=['POST'])
def update_friend_statistic() -> flask.Response:
    """
    Update statistics of online games of user.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    token = jwt.decode(request.cookies['token'], app.secret_key, algorithms=['HS256'])
    user_id = token['user_id']
    data = request.get_json()
    games_played = data['games_played']
    games_won = data['games_won']
    games_draws = data['games_draws']
    games_defeat = data['games_defeat']

    user = OnlineGameStat.query.filter_by(id=user_id).first()

    user.games_played = games_played
    user.games_won = games_won
    user.games_draws = games_draws
    user.games_defeat = games_defeat

    db.session.commit()

    return jsonify({'message': 'Game statistics updated successfully'})


@app.route('/reset_search', methods=['GET'])
def reset_search() -> flask.Response:
    """
    Reset the game search.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    token = jwt.decode(request.cookies['token'], app.secret_key, algorithms=['HS256'])
    user_id = token['user_id']
    for elem in waiting_players:
        if elem['user_id'] == user_id:
            waiting_players.remove(elem)
            break

    return jsonify({'message': 'Success search reset'})


@socketio.on('connect')
def on_connect(*args) -> None:
    """Connect the user to the game."""
    game_id = request.args.get('game_id')
    user_id = request.args.get('user_id')

    users_dict[user_id] = request.sid

    join_room(game_id)

    if user_id == games[game_id]['player1']['id']:
        user = User.query.filter_by(id=games[game_id]['player2']['id']).first()
        emit('info', {"message": "Your turn", "sign": games[game_id]['player1']['sign'],
                      "opponent": user.username, "opponent_id": games[game_id]['player2']['id'],
                      "opponent_sign": games[game_id]['player2']['sign']},
             room=game_id, to=users_dict[user_id])
    elif user_id == games[game_id]['player2']['id']:
        user = User.query.filter_by(id=games[game_id]['player1']['id']).first()
        emit('info', {"message": "Not your turn", "sign": games[game_id]['player2']['sign'],
                      "opponent": user.username, "opponent_id": games[game_id]['player1']['id'],
                      "opponent_sign": games[game_id]['player1']['sign']},
             room=game_id, to=users_dict[user_id])


@socketio.on('check_opponent')
def check_opponent(data: Dict[str, str]) -> None:
    """
    Check if the opponent is in the game.

    Tell the user that it is possible to start the game, or tells the user that the opponent reset the game.

    :param data: Dictionary with game parameters
    :type data: class: `dict[str, str]`
    """
    game_id = data['game_id']
    user_id = data['user_id']
    opponent_id = data['opponent_id']

    if opponent_id not in users_dict:
        emit('opponent_reset', room=game_id, to=users_dict[user_id])
    else:
        emit('start_game', room=game_id, to=users_dict[opponent_id])


@socketio.on('play')
def on_play(data: Dict[str, Union[str, int]]) -> None:
    """
    Inform the opponent about the user's progress.

    :param data: Dictionary with game parameters
    :type data: class: `dict[str, str | int]`
    """
    game_id = data['game_id']
    pos = data['pos']
    user_id = data['user_id']
    opponent_id = data['opponent_id']

    users = list(socketio.server.manager.rooms['/'][game_id])

    if len(users) == 1:
        emit('opponent_reset', room=game_id, to=users_dict[user_id])
    else:
        emit('update_board', {"pos": pos}, room=game_id, to=users_dict[opponent_id])


@socketio.on('leave')
def leave(data: Dict[str, str]) -> None:
    """
    Exit the game at the end of it.

    :param data: Dictionary with game parameters
    :type data: class: `dict[str, str]`
    """
    game_id = data['game_id']
    user_id = data['user_id']
    if len(socketio.server.manager.rooms['/'][game_id]) == 1:
        games.pop(game_id)
    leave_room(game_id)
    leave_room(users_dict[user_id])
    leave_room(None)
    users_dict.pop(user_id)


@socketio.on('game_over')
def game_over(data: Dict[str, Union[str, bool, int]]) -> None:
    """
    Tell the opponent that the game is over.

    :param data: Dictionary with game parameters
    :type data: class: `dict[str, str | bool | int]`
    """
    game_id = data['game_id']
    is_draw = data['is_draw']
    opponent_id = data['opponent_id']
    pos = data['pos']

    if not is_draw:
        pos_a = data['a']
        pos_b = data['b']
        pos_c = data['c']
        emit('update_game_over', {'is_draw': is_draw, 'a': pos_a, 'b': pos_b, 'c': pos_c, 'pos': pos},
             room=game_id, to=users_dict[opponent_id])
    else:
        emit('update_game_over', {'is_draw': is_draw, 'pos': pos}, room=game_id, to=users_dict[opponent_id])


@socketio.on('reset_game')
def reset_game(data: Dict[str, str]) -> None:
    """
    Cancel the game for the user.

    :param data: Dictionary with game parameters
    :type data: class: `dict[str, str]`
    """
    game_id = data['game_id']
    user_id = data['user_id']
    opponent_id = data['opponent_id']

    emit('opponent_reset', room=game_id, to=users_dict[opponent_id])
    leave_room(game_id)
    leave_room(users_dict[user_id])
    leave_room(None)
    users_dict.pop(user_id)


@app.route('/is_game_searched', methods=['GET'])
def is_game_searched() -> flask.Response:
    """
    Tell if a game has been found for the user.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    data = jwt.decode(request.cookies['token'], app.secret_key, algorithms=['HS256'])
    user_id = data['user_id']

    flag = False

    for elem in waiting_players:
        if elem['user_id'] == user_id:
            flag = True

    if not flag:
        for key, elem in games.items():
            if elem['player1']['id'] == user_id:
                return jsonify({'message': 'Success', 'opponent': elem['player2']['id'], 'game_id': key})
            elif elem['player2']['id'] == user_id:
                return jsonify({'message': 'Success', 'opponent': elem['player1']['id'], 'game_id': key})

    return jsonify({'message': 'Game is not searched yet'})


@app.route('/join_queue', methods=['POST'])
def join_queue() -> flask.Response:
    """
    Add a user to the list of users who are looking for a game.

    :return: Server response
    :rtype: class: `flask.Response`
    """
    token = jwt.decode(request.cookies['token'], app.secret_key, algorithms=['HS256'])
    user_id = token['user_id']
    data = request.get_json()
    if data['sign'] == 'R':
        data['sign'] = random.choice(['X', 'O'])

    if data['turn'] == '0':
        data['turn'] = random.choice(['1', '2'])

    waiting_players.append({'user_id': user_id, 'sign': data['sign'], 'turn': data['turn']})

    return jsonify({'message': 'Success'})


if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('game.db'):
            db.create_all()
    socketio.run(app)
