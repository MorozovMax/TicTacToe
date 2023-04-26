"""A module with a computer game class page and an online game class page."""

import tkinter as tk
import os
import sys
import random
import json
import gettext
from typing import Tuple, List, Optional, Dict, Callable, Union
import pygame as pg
import requests
import socketio
import setting_page as setp


translation = gettext.translation('tictactoe',
                                  os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
                                               'locale'),
                                  fallback=True)


class FriendGame(tk.Frame):
    """
    The online game class page.

    :param master: An instance of the main class of the game application
    :type master: class: `tictactoe.App`
    """

    def __init__(self, master) -> None:
        """Constructor method."""
        super().__init__(master)

        if not self.master.mute_flag:
            self.master.background_music.set_volume(0.3)

        self.configure(height=650, width=550)
        self.pack_propagate(False)

        self._cur_music: pg.mixer.Sound = self.master.win_music

        if not self.master.lang_flag:
            self._: Callable = lambda s: s
        else:
            self._: Callable = translation.gettext

        self._status_msg: str = 'Waiting for the opponent'

        self.master.cur_page = 'Game_page_fr'

        self.turn: Optional[str] = None
        self.sign: Optional[str] = None
        self.opponent_sign: Optional[str] = None
        self.opponent: Optional[str] = None
        self.opponent_id: Optional[str] = None
        self.is_draw_flag: bool = False
        self.opponent_reset: bool = False

        self.master.now_game = True

        self.sio: socketio.Client = socketio.Client()
        self.master.sio = self.sio
        self.sio.on('info', self.on_info)
        self.sio.on('start_game', self.on_start_game)
        self.sio.on('opponent_reset', self.on_opponent_reset)
        self.sio.on('update_game_over', self.on_update_game_over)
        self.sio.on('update_board', self.on_update_board)
        self.sio.connect('http://localhost:5000', headers={'game_id': self.master.game_id,
                                                           'user_id': self.master.user_id})

        self._user1_sign: Optional[str] = self.sign
        self._user2_sign: Optional[str] = self.opponent_sign
        self._user1: str = self.master.user
        self._user2: Optional[str] = self.opponent
        self._player_sign_msg: str = f"{self.master.user}:  {self._user1_sign}       {self._user2}:  {self._user2_sign}"

        self._free_squares: List[int] = list(range(9))
        self._win_pos: Tuple[Tuple[int, ...], ...] = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                                                      (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self._color: Dict[str, str] = {"X": "red", "O": "blue"}
        self._end_game: bool = False
        self._return_btn_flag: bool = False
        self.turn_flag: bool = False
        self.win_flag: bool = False
        self.start_flag: bool = False
        self._return_btn: tk.Button = tk.Button()
        self._status: tk.Label = tk.Label()
        self._field: List[tk.Button] = [tk.Button()]

        self._create_widgets()

        self.after(10000, lambda: self.sio.emit('check_opponent', data={'game_id': self.master.game_id,
                                                                        'user_id': self.master.user_id,
                                                                        'opponent_id': self.opponent_id}))

    def on_start_game(self) -> None:
        """
        A method that receives a message from the server about the start of the game
        and prepares the field and status messages so that you can start the game.
        """
        self.start_flag = True

        if self.turn == "Your turn":
            self.turn_flag = True
            self._status_msg = self._("Now your turn")
            self._status.config(text=self._status_msg)
            for elem in self._field:
                elem["state"] = "normal"
        else:
            self.turn_flag = False
            self._status_msg = self._("Waiting for the opponent turn")
            self._status.config(text=self._status_msg)

        self._return_btn.config(state='normal')

    def on_update_game_over(self, data: Dict[str, Union[str, int, bool]]) -> None:
        """
        A method that performs actions to end the game if the opponent wins.

        :param data: Dictionary with data about the end of the game
        :type data: class `dict[str, str | int | bool]`
        """
        is_draw = bool(data['is_draw'])
        square = data['pos']
        self._field[square]["text"] = self.opponent_sign
        self._field[square]["disabledforeground"] = self._color[self.opponent_sign]
        self._free_squares.remove(square)

        if is_draw:
            self._end_game = True
            self.is_draw_flag = True
            self._status_msg = self._("It is a draw")
            self._status.config(text=self._status_msg)
            self._cur_music = self.master.draw_music
            for elem in self._field:
                elem["background"] = "#F0E68C"
            self.sio.emit('leave', data={'game_id': self.master.game_id, 'user_id': self.master.user_id})
            self._update_statistic(0)
            self.master.now_game = False
            self._bind_return_btn()
        else:
            self.master.defeat_music.play()
            pos_a = data['a']
            pos_b = data['b']
            pos_c = data['c']
            self._end_game = True
            self.win_flag = False
            self._status_msg = self._("{player} win").format(player=self.opponent)
            self._status.config(text=self._status_msg)
            self._field[pos_a]["background"], self._field[pos_b]["background"], self._field[pos_c]["background"] = \
                "#F08080", "#F08080", "#F08080"
            for elem in self._free_squares:
                self._field[elem]["state"] = "disabled"
            self._status["text"] = self._status_msg
            self._status.config(fg='red')
            self.sio.emit('leave', data={'game_id': self.master.game_id, 'user_id': self.master.user_id})
            self._update_statistic(2)
            self.master.now_game = False
            self._bind_return_btn()

    def on_update_board(self, data: Dict[str, int]) -> None:
        """
        A method that performs actions to update the field and status messages after the opponent's move.

        :param data: Dictionary with the information about the opponent turn from the server
        :type data: class: `dict[str, int]`
        """
        square = data['pos']
        self._field[square]["text"] = self.opponent_sign
        self._field[square]["disabledforeground"] = self._color[self.opponent_sign]
        self._free_squares.remove(square)
        self.turn_flag = True
        self._status_msg = self._("Now your turn")
        self._status["text"] = self._status_msg
        self.master.click_music.play()
        for elem in self._free_squares:
            self._field[elem]["state"] = "normal"

    def on_opponent_reset(self) -> None:
        """A method that performs actions if the opponent has left the game."""
        self.master.win_music.play()
        self._end_game = True
        self.opponent_reset = True
        self._status_msg = self._("{player} reset the game").format(player=self.opponent)
        for elem in self._free_squares:
            self._field[elem]["state"] = "disabled"
        self._status["text"] = self._status_msg
        self._status.config(fg='green')
        self.sio.emit('leave', data={'game_id': self.master.game_id, 'user_id': self.master.user_id})
        self._update_statistic(1)
        self.master.now_game = False
        self._bind_return_btn()

    def on_info(self, data: Dict[str, str]) -> None:
        """
        A method that takes information about the game from the server and saves it.

        :param data: Dictionary with the information about the game from the server
        :type data: class: `dict[str, str]`
        """
        self.turn = data['message']
        self.sign = data['sign']
        self.opponent = data['opponent']
        self.opponent_id = data['opponent_id']
        self.master.opponent_id = self.opponent_id
        self.opponent_sign = data['opponent_sign']

    def _click(self, square: int) -> None:
        """
        A method with an action for a button that is an element of the game field.

        :param square: The position chosen by the player
        :type square: class `int`
        """
        self.master.click_music.play()
        self._draw_sign(square)
        self._free_squares.remove(square)
        for elem in self._free_squares:
            self._field[elem]["state"] = "disabled"
        result = self._check_win()
        self._if_end_game(result, square)
        self._change_status()
        if not self._end_game:
            self.sio.emit('play', data={'game_id': self.master.game_id, 'pos': square,
                                        'user_id': self.master.user_id, 'opponent_id': self.opponent_id})

    def _set_end_game(self, pos_a: int, pos_b: int, pos_c: int) -> None:
        """
        The method that sets the end of the game, tells which player won
        and repaints the field in the appropriate color.

        :param pos_a: The first of three positions from which a win is obtained
        :type pos_a: class: `int`
        :param pos_b: The second of the three positions from which a win is obtained
        :type pos_b: class: `int`
        :param pos_c: The third of the three positions from which a win is obtained
        :type pos_c: class: `int`
        """
        self._end_game = True
        self._status_msg = self._("{player} win").format(player=self.master.user)
        self.win_flag = True
        self._field[pos_a]["background"], self._field[pos_b]["background"], self._field[pos_c]["background"] = \
            self._end_game_color()

    def _if_drawn_game(self) -> None:
        """A method that checks whether the game ended in a draw and performs the appropriate actions."""
        if not self._free_squares:
            self._end_game = True
            self.is_draw_flag = True
            self._status_msg = self._("It is a draw")
            self._cur_music = self.master.draw_music
            for elem in self._field:
                elem["background"] = "#F0E68C"
            self._update_statistic(0)

    def _check_win(self) -> Optional[Tuple[int, int, int]]:
        """
        The method that checks whether the game ended with a victory for player,
        otherwise causes a check for a draw.

        :return: A tuple with a player's winning position or None
        :rtype: class: `tuple[int, int, int]` or None
        """
        for pos_a, pos_b, pos_c in self._win_pos:
            if (self._field[pos_a]["text"] == self.sign) and (self._field[pos_b]["text"] == self.sign) and \
               (self._field[pos_c]["text"] == self.sign):
                self._set_end_game(pos_a, pos_b, pos_c)
                self._update_statistic(1)
                return pos_a, pos_b, pos_c

        self._if_drawn_game()
        return None

    def _if_end_game(self, result: Optional[Tuple], square: int) -> None:
        """
        A method that performs the actions to be performed if the game is over
        and sends a message to the server that the game is finished.

        :param result: A tuple with a player's winning position
        :type result: class: `tuple` or None
        :param square: The position that the player went to and which led to the end of the game
        :type square: class: `int`
        """
        if self._end_game:
            self._cur_music.play()
            for elem in self._free_squares:
                self._field[elem]["state"] = "disabled"
            self._status["text"] = self._status_msg
            if not self.is_draw_flag:
                self._status.config(fg='green')
            if result is None:
                self.sio.emit('game_over', data={'game_id': self.master.game_id, 'pos': square,
                                                 'opponent_id': self.opponent_id, 'is_draw': self.is_draw_flag})
            else:
                self.sio.emit('game_over', data={'game_id': self.master.game_id, 'pos': square,
                                                 'opponent_id': self.opponent_id, 'is_draw': self.is_draw_flag,
                                                 'a': result[0], 'b': result[1], 'c': result[2]})
            self.sio.emit('leave', data={'game_id': self.master.game_id, 'user_id': self.master.user_id})
            self.master.now_game = False
            self._bind_return_btn()

    def _draw_sign(self, square: int) -> None:
        """
        A method that draws a player sign at the position he has chosen.

        :param square: The position chosen by the player
        :type square: class `int`
        """
        self._field[square]["state"] = "disabled"
        self._field[square]["text"] = self.sign
        self._field[square]["disabledforeground"] = self._color[self.sign]

    def _switch_frame(self) -> None:
        """A method with action for the "Return to online game page" button."""
        self.after(500, self.sio.disconnect)
        self._return_btn["state"] = "disabled"
        self.after(1000, lambda: self.master.switch_frame(setp.FriendStartPage))

    def _bind_return_btn(self) -> None:
        """A method that changes a "Reset game" button to a "Return to online game page" button."""
        self._return_btn_flag = True
        self._return_btn["text"] = self._("Return to online game page")
        self._return_btn["command"] = self._switch_frame
        self._return_btn["state"] = "normal"

    def _change_status(self) -> None:
        """
        A method that changes the text of the label with the status
        of the game to "Waiting for the opponent turn".
        """
        if not self._end_game:
            self.turn_flag = False
            self._status_msg = self._("Waiting for the opponent turn")
            self._status["text"] = self._status_msg

    @staticmethod
    def _end_game_color() -> Tuple[str, str, str]:
        """
        A method that sets the color of the field illumination after the end of the game.

        :return: Tuple of three same color strings of the field illumination after the end of the game
        :rtype: class `tuple[str, str, str]`
        """
        return "#90EE90", "#90EE90", "#90EE90"

    def _update_statistic(self, flag: int) -> None:
        """
        A method that updates statistics and sends them to the server.

        :param flag: Flag signaling the outcome of the game; 0 - drawn, 1 - win, 2 - defeat
        :type flag: class: `int`
        """
        if flag == 0:
            self.master.friend_stat["drawn_game"] += 1
        elif flag == 1:
            self.master.friend_stat["Player1_win"] += 1
        elif flag == 2:
            self.master.friend_stat["Player2_win"] += 1

        url = 'http://localhost:5000/update_friend_statistic'
        headers = {'Content-Type': 'application/json'}
        data = {'games_played': self.master.friend_stat["Player1_win"] + self.master.friend_stat["Player2_win"] +
                self.master.friend_stat["drawn_game"],
                'games_won': self.master.friend_stat['Player1_win'],
                'games_draws': self.master.friend_stat['drawn_game'],
                'games_defeat': self.master.friend_stat['Player2_win']}
        requests.post(url, headers=headers, data=json.dumps(data), cookies=self.master.token)

    def _status_lbl(self) -> None:
        """Method for drawing a label with the game status."""
        self._status = tk.Label(self, bg="white", font=self.master.font, text=self._status_msg, width=36, height=2)
        self._status.pack(side="top", pady=15)

    def _create_field(self, frame: tk.Frame) -> List[tk.Button]:
        """
        Method for drawing the playing field from buttons.

        :param frame: Frame for drawing the playing field from buttons
        :type frame: class `tkinter.Frame`
        :return: Game field
        :rtype: class `list[tkinter.Button]`
        """
        field = []
        for i in range(9):
            button = tk.Button(frame, text=' ', width=3, height=2, font=('Verdana', 45, 'bold'),
                               background='white', command=lambda square=i: self._click(square),  # type: ignore
                               state="disabled")
            button.grid(row=i // 3, column=i % 3, sticky='nsew')
            field.append(button)

        return field

    def _player_sign_lbl(self) -> None:
        """Method for drawing label with the names of players and their signs."""
        tk.Label(self, font=self.master.font, text=self._player_sign_msg).pack(
            side="top", anchor="n", pady=(10, 15))

    def _create_widgets(self) -> None:
        """The method of rendering widgets of the online game page."""
        self._player_sign_lbl()

        frame = tk.Frame(self)
        frame.pack(side="top")

        self._field = self._create_field(frame)
        self._status_lbl()
        self._create_return_btn()

    def _create_return_btn(self) -> None:
        """The method of rendering "Reset game" button."""
        self._return_btn = tk.Button(self, bg="white", font=self.master.btn_font, text=self._("Reset game"),
                                     command=self.reset_game, state='disabled', width=30)
        self._return_btn.pack(side="top", pady=(0, 15))

    def reset_game(self) -> None:
        """A method with action for the "Reset game" button."""
        self.master.defeat_music.play()
        self._update_statistic(2)
        self.sio.emit('reset_game', data={'game_id': self.master.game_id, 'user_id': self.master.user_id,
                                          'opponent_id': self.opponent_id})

        self._switch_frame()

    def change_language(self, lang: str) -> None:
        """
        Method with action for the language change button.

        :param lang: A string with the localization language of the application, "en" or "ru"
        :type lang: class: `str`
        """
        if lang == 'ru':
            self._ = translation.gettext
        else:
            self._ = lambda s: s

        self.master.title(self._("Tic-Tac-Toe"))
        if not self._return_btn_flag:
            self._return_btn.config(text=self._("Reset game"))
        else:
            self._return_btn.config(text=self._("Return to online game page"))

        if self._end_game:
            if self.is_draw_flag:
                self._status.config(text=self._("It is a draw"))
            elif self.opponent_reset:
                self._status.config(text=self._("{player} reset the game").format(player=self.opponent))
            else:
                if self.win_flag:
                    self._status.config(text=self._("{player} win").format(player=self.opponent))
                else:
                    self._status.config(text=self._("{player} win").format(player=self.master.user))
        else:
            if self.start_flag:
                if self.turn_flag:
                    self._status.config(text=self._("Now your turn"))
                else:
                    self._status.config(text=self._("Waiting for the opponent turn"))
            else:
                self._status.config(text=self._('Waiting for the opponent'))


class PcGame(tk.Frame):
    """
    The computer game class page.

    :param master: An instance of the main class of the game application
    :type master: class: `tictactoe.App`
    """

    def __init__(self, master) -> None:
        """Constructor method."""
        super().__init__(master)

        self.configure(height=650, width=550)
        self.pack_propagate(False)

        self._cur_music: pg.mixer.Sound = self.master.win_music

        self.master.cur_page = 'Game_page_pc'

        if not self.master.lang_flag:
            self._: Callable = lambda s: s
        else:
            self._: Callable = translation.gettext

        self._status_msg: str = self._('Press "Start" button to start the game')
        self._user1_sign, self._user2_sign = self._sign_choose()
        self._user1, self._user2 = self._player_name()
        self._player_sign_msg: str = f"{self.master.user}:  {self._user1_sign}       {self._user2}:  {self._user2_sign}"

        self._cur_sign, self._cur_player = self._begin_cur_sign()

        self._free_squares: List[int] = list(range(9))
        self._win_pos: Tuple[Tuple[int, ...], ...] = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                                                      (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self._color: Dict[str, str] = {"X": "red", "O": "blue"}
        self._end_game: bool = False
        self._is_draw: bool = False
        self._return_btn_flag: bool = False
        self._return_btn: tk.Button = tk.Button()
        self._status: tk.Label = tk.Label()
        self._field: List[tk.Button] = [tk.Button()]

        self.master.now_game = False

        self._create_widgets()

        self._choice_pc1: List[int] = [0, 2, 6, 8]
        self._choice_pc2: List[int] = [1, 3, 5, 7]
        self._choice_pc: Optional[List[int]] = None

    def _cur_sign_change(self) -> Tuple[str, str]:
        """
        A function that changes the name and badge of the current player to another.

        :return: Current player name and current player sign
        :rtype: class: `tuple[str, str]`
        """
        if self._cur_sign == "X":
            sign = "O"
        else:
            sign = "X"

        if self._cur_player == self._user1:
            player = self._user2
        else:
            player = self._user1

        return sign, player

    def _status_lbl(self) -> None:
        """Method for drawing a label with the game status."""
        self._status = tk.Label(self, bg="white", font=self.master.font, text=self._status_msg, width=36, height=2)
        self._status.pack(side="top", pady=15)

    def _create_field(self, frame: tk.Frame) -> List[tk.Button]:
        """
        Method for drawing the playing field from buttons.

        :param frame: Frame for drawing the playing field from buttons
        :type frame: class `tkinter.Frame`
        :return: Game field
        :rtype: class `list[tkinter.Button]`
        """
        field = []
        for i in range(9):
            button = tk.Button(frame, text=' ', width=3, height=2, font=('Verdana', 45, 'bold'),
                               background='white', command=lambda square=i: self._click(square),
                               state="disabled")
            button.grid(row=i // 3, column=i % 3, sticky='nsew')
            field.append(button)

        return field

    def _player_sign_lbl(self) -> None:
        """Method for drawing label with the names of players and their signs."""
        tk.Label(self, font=self.master.font, text=self._player_sign_msg).pack(
            side="top", anchor="n", pady=(10, 15))

    def _create_widgets(self) -> None:
        """The method of rendering widgets of the computer game page."""
        self._player_sign_lbl()

        frame = tk.Frame(self)
        frame.pack(side="top")

        self._field = self._create_field(frame)
        self._status_lbl()
        self._create_return_btn()

    def _create_return_btn(self) -> None:
        """The method of rendering "Start" button for starting the game."""
        self._return_btn = tk.Button(self, bg="white", font=self.master.btn_font, text=self._("Start"),
                                     command=self._start_game, width=30)
        self._return_btn.pack(side="top", pady=(0, 15))

    def _begin_cur_sign(self) -> Optional[Tuple[str, str]]:
        """
        A method that selects the sign and player name of the player who moves first.

        :return: The sign and player name of the player who moves first or None
        :rtype: class `tuple[str, str]` or None
        """
        if self.master.move.get() == 1:
            return self._user1_sign, self._user1
        elif self.master.move.get() == 2:
            return self._user2_sign, self._user2
        elif self.master.move.get() == 0:
            i = random.randint(0, 1)
            return [self._user1_sign, self._user2_sign][i], [self._user1, self._user2][i]

        return None

    def _sign_choose(self) -> Optional[Tuple[str, str]]:
        """
        A method that sets signs for players.

        :return: Signs for players or None
        :rtype: class `tuple[str, str]` or None
        """
        if self.master.sign.get() == "R":
            i = random.randint(0, 1)
            return ["X", "O"][i], ["X", "O"][1 - i]
        elif self.master.sign.get() == "X":
            return "X", "O"
        elif self.master.sign.get() == "O":
            return "O", "X"

        return None

    def _switch_frame(self) -> None:
        """
        A method that sends statistics to the server and changes the page
        to the settings page of the game with the computer.
        """
        url = 'http://localhost:5000/update_computer_statistic'
        headers = {'Content-Type': 'application/json'}
        data = {'games_played': self.master.pc_stat["Player_win"] + self.master.pc_stat["Computer_win"] +
                self.master.pc_stat["drawn_game"],
                'games_won': self.master.pc_stat['Player_win'],
                'games_draws': self.master.pc_stat['drawn_game'], 'games_defeat': self.master.pc_stat['Computer_win']}
        requests.post(url, headers=headers, data=json.dumps(data), cookies=self.master.token)
        self.master.switch_frame(setp.PcStartPage)

    def _bind_return_btn(self) -> None:
        """A method that changes the label and action for the "Start" button."""
        self._return_btn_flag = True
        self._return_btn["text"] = self._("Return to configure page")
        self._return_btn["command"] = self._switch_frame
        self._return_btn["state"] = "disabled"

    @staticmethod
    def _player_name() -> Tuple[str, str]:
        """
        A method that returns a tuple of the strings "Player" and "Computer".

        :return: The tuple of the strings "Player" and "Computer"
        :rtype: class: `tuple[str, str]`
        """
        return "Player", "Computer"

    def _precondition(self) -> None:
        """A method that makes the playing field active and informs that the game has started."""
        for elem in self._field:
            elem["state"] = "normal"
        self._status_msg = self._("The game has started")
        self._status["text"] = self._status_msg

    def _change_sign_and_status(self) -> None:
        """A method that changes the sign and name of the current player."""
        if not self._end_game:
            self._cur_sign, self._cur_player = self._cur_sign_change()

    def _end_game_color(self) -> Tuple[str, str, str]:
        """
        A method that sets the color of the field illumination after the end of the game.

        :return: Tuple of three same color strings of the field illumination after the end of the game
        :rtype: class `tuple[str, str, str]`
        """
        if self._cur_player == "Player":
            return "#90EE90", "#90EE90", "#90EE90"
        else:
            return "#F08080", "#F08080", "#F08080"

    def _set_end_game_music(self) -> None:
        """A method that sets the music of the end of the game depending on the outcome of the game."""
        if self._cur_player == "Player":
            self._cur_music = self.master.win_music
        else:
            self._cur_music = self.master.defeat_music

    def _update_statistic(self, flag: bool) -> None:
        """
        A method that updates player statistics.

        :param flag: Flag indicating whether the game ended in a draw
        :type flag: class `bool`
        """
        if flag:
            self.master.pc_stat[self._cur_player + "_win"] += 1
        else:
            self.master.pc_stat["drawn_game"] += 1

    def _start_game_1(self) -> None:
        """A method that performs actions to start the game."""
        self.master.click_music.play()
        self._precondition()
        self._bind_return_btn()

    def _draw_sign(self, square: int) -> None:
        """
        A method that draws a player's sign at the position he has chosen.

        :param square: The position chosen by the player
        :type square: class `int`
        """
        self._field[square]["state"] = "disabled"
        self._field[square]["text"] = self._cur_sign
        self._field[square]["disabledforeground"] = self._color[self._cur_sign]

    def _if_end_game(self) -> None:
        """A method that performs the actions to be performed if the game is over."""
        if self._end_game:
            self._cur_music.play()
            for elem in self._free_squares:
                self._field[elem]["state"] = "disabled"
            self._status["text"] = self._status_msg
            self.master.now_game = False
            self._return_btn["state"] = "normal"

    def _click_1(self, square: int) -> None:
        """
        A method that performs actions corresponding to the player's turn.

        :param square: The position chosen by the player
        :type square: class `int`
        """
        self.master.click_music.play()
        self._draw_sign(square)
        self._free_squares.remove(square)
        self._check_win()
        self._change_sign_and_status()
        self._if_end_game()

    def _set_end_game(self, pos_a: int, pos_b: int, pos_c: int) -> None:
        """
        The method that sets the end of the game, tells which player won
        and repaints the field in the appropriate color.

        :param pos_a: The first of three positions from which a win is obtained
        :type pos_a: class: `int`
        :param pos_b: The second of the three positions from which a win is obtained
        :type pos_b: class: `int`
        :param pos_c: The third of the three positions from which a win is obtained
        :type pos_c: class: `int`
        """
        self._end_game = True
        self._set_end_game_music()
        if self._cur_player == "Computer":
            self._status_msg = self._("{player} win").format(player=self._cur_player)
        else:
            self._status_msg = self._("{player} win").format(player=self.master.user)
        self._field[pos_a]["background"], self._field[pos_b]["background"], self._field[pos_c]["background"] = \
            self._end_game_color()

    def _if_drawn_game(self) -> None:
        """A method that checks whether the game ended in a draw and performs the appropriate actions."""
        if not self._free_squares:
            self._end_game = True
            self._is_draw = True
            self._status_msg = self._("It is a draw")
            self._cur_music = self.master.draw_music
            for elem in self._field:
                elem["background"] = "#F0E68C"
            self._update_statistic(False)

    def _check_win(self) -> None:
        """
        The method that checks whether the game ended with a victory for the computer or the player,
        otherwise causes a check for a draw.
        """
        for pos_a, pos_b, pos_c in self._win_pos:
            if (self._field[pos_a]["text"] == self._cur_sign) and (self._field[pos_b]["text"] == self._cur_sign) and \
               (self._field[pos_c]["text"] == self._cur_sign):
                self._set_end_game(pos_a, pos_b, pos_c)
                self._update_statistic(True)
                return

        self._if_drawn_game()

    def _is_win(self, sign: str, field: List[str]) -> bool:
        """
        A method that checks whether there is a winning position on field for a given sign.

        :param sign: Sign of player or computer
        :type sign: class: `str`
        :param field: List of signs on specific positions
        :type field: class `list[str]`
        :return: Flag of whether there is a winning position
        :rtype: class: `bool`
        """
        for pos_a, pos_b, pos_c in self._win_pos:
            if field[pos_a] == sign and field[pos_b] == sign and field[pos_c] == sign:
                return True

        return False

    def _find_best_turn(self, sign: str) -> Optional[int]:
        """
        A method that finds position of the best turn for computer.

        :param sign: Sign of player or computer
        :type sign: class `str`
        :return: Position of the best turn or None
        :rtype: class `int` or None
        """
        for i in self._free_squares:
            field = [elem["text"] for elem in self._field]
            field[i] = sign
            result = self._is_win(sign, field)
            if result:
                return i

        return None

    def _default_choice(self) -> Optional[int]:
        """
        A method that randomly selects a position for the computer's move if the best move has not been found.

        :return: Random position of the computer turn or None
        :rtype: class `int` or None
        """
        if self._choice_pc is None:
            self._choice_pc = [4]
            random.shuffle(self._choice_pc1)
            random.shuffle(self._choice_pc2)
            self._choice_pc.extend(self._choice_pc1)
            self._choice_pc.extend(self._choice_pc2)

        for i in self._choice_pc:
            if i in self._free_squares:
                return i

        return None

    def _computer_turn(self) -> None:
        """A method that selects a position for the computer's move and executes a move to that position."""
        square = self._find_best_turn(self._user2_sign)
        if square is None:
            square = self._find_best_turn(self._user1_sign)
            if square is None:
                square = self._default_choice()

        self._turn(square)

    def _turn(self, square: int) -> None:
        """
        A method that performs actions corresponding to the computer's turn.

        :param square: The position chosen by the computer
        :type square: class `int`
        """
        self._draw_sign(square)
        self._free_squares.remove(square)
        self._check_win()
        self._change_sign_and_status()
        self._if_end_game()

    def _start_game(self) -> None:
        """Method with action for the "Start" button."""
        self.master.now_game = True
        self._start_game_1()
        if self._cur_player == "Computer":
            self._computer_turn()

    def _click(self, square: int) -> None:
        """
        A method with an action for a button that is an element of the game field
        and that passes the move to the computer, if the game is not over.

        :param square: The position chosen by the player
        :type square: class `int`
        """
        self._click_1(square)
        if not self._end_game:
            self._computer_turn()

    def change_language(self, lang: str) -> None:
        """
        Method with action for the language change button.

        :param lang: A string with the localization language of the application, "en" or "ru"
        :type lang: class: `str`
        """
        if lang == 'ru':
            self._ = translation.gettext
        else:
            self._ = lambda s: s

        self.master.title(self._("Tic-Tac-Toe"))
        if not self._return_btn_flag:
            self._return_btn.config(text=self._("Start"))
            self._status.config(text=self._('Press "Start" button to start the game'))
        else:
            self._return_btn.config(text=self._("Return to configure page"))
            if self._end_game:
                if self._is_draw:
                    self._status.config(text=self._("It is a draw"))
                else:
                    if self._cur_player == "Computer":
                        self._status.config(text=self._("{player} win").format(player=self._cur_player))
                    else:
                        self._status.config(text=self._("{player} win").format(player=self.master.user))
            else:
                self._status.config(text=self._("The game has started"))
