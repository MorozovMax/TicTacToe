"""
A module with the main class of the game application.
Also, the application is launched in this module, and the necessary
actions are performed after closing the application.
"""

import tkinter as tk
import tkinter.font as tkfont
import sys
import os
import pickle
import json
import gettext
from pathlib import Path
from typing import Union, Dict, Callable, Optional
import pygame as pg
import requests
import socketio
from PIL import Image, ImageTk
import start_page as stp
import setting_page as setp
import search_game_page as sgp
import game_page as gap


translation = gettext.translation('tictactoe',
                                  os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
                                               'locale'),
                                  fallback=True)


class App(tk.Tk):
    """The main class of the game application."""

    def __init__(self) -> None:
        """Constructor method."""
        super().__init__()

        self._: Callable = lambda s: s

        self.title(self._("Tic-Tac-Toe"))
        self.resizable(False, False)

        self._frame: Union[None, stp.StartPage, setp.FriendStartPage,
                           setp.PcStartPage, gap.FriendGame, gap.PcGame,
                           sgp.SearchGamePage] = None

        self.font: tkfont.Font = tkfont.Font(size=14, weight="bold", slant="italic")
        self.btn_font: tkfont.Font = tkfont.Font(size=12, weight="normal", slant="italic")

        path1 = self.resource_path("images")
        path2 = self.resource_path("music")

        self.tictactoe_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1,
                                                                                      "TicTacToe.png")).resize((350,
                                                                                                                350)))
        self._mute_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1,
                                                                                  "mute.png")).resize((30, 30)))
        self._unmute_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1,
                                                                                    "unmute.png")).resize((30, 30)))

        self._en_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1,
                                                                                "EN.png")).resize((30, 30)))
        self._ru_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1,
                                                                                "RU.png")).resize((30, 30)))

        self.hide_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1, "hide.png")).resize((20, 20)))
        self.show_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1, "show.png")).resize((20, 20)))

        self.friend_stat: Dict[str, int] = {"drawn_game": 0, "Player1_win": 0, "Player2_win": 0}
        self.pc_stat: Dict[str, int] = {"drawn_game": 0, "Player_win": 0, "Computer_win": 0}

        self.sign: tk.StringVar = tk.StringVar()
        self.move: tk.IntVar = tk.IntVar()
        self.sign.set("_")
        self.move.set(-1)

        pg.init()
        pg.mixer.init(44100, -16, 1, 512)

        self.background_music: pg.mixer.Sound = pg.mixer.Sound(Path(path2, "music.mp3"))
        self.click_music: pg.mixer.Sound = pg.mixer.Sound(Path(path2, "click.mp3"))
        self.background_music.set_volume(0.3)
        self.click_music.set_volume(1)

        self.find_music: pg.mixer.Sound = pg.mixer.Sound(Path(path2, "find.mp3"))
        self.find_music.set_volume(0.5)

        self.win_music: pg.mixer.Sound = pg.mixer.Sound(Path(path2, "win.mp3"))
        self.win_music.set_volume(0.6)
        self.defeat_music: pg.mixer.Sound = pg.mixer.Sound(Path(path2, "defeat.mp3"))
        self.defeat_music.set_volume(0.2)
        self.draw_music: pg.mixer.Sound = pg.mixer.Sound(Path(path2, "draw.wav"))
        self.draw_music.set_volume(0.3)

        self.mute_flag: bool = False
        self.lang_flag: bool = False
        self.token = None

        self.user_id: Optional[str] = None
        self.opponent_id: Optional[str] = None
        self.game_id: Optional[str] = None

        self.sio: Optional[socketio.Client] = None

        self.cur_page: Optional[str] = None
        self.now_game: bool = False

        self.background_music.play(-1)

        try:
            with open('token.pickle', 'rb') as file:
                self.token = pickle.load(file)

            _url = 'http://localhost:5000/'
            _response = requests.get(_url, cookies=self.token)

            self.remember_login: bool = True
            self.user: str = _response.json()['user']
            self.pc_stat['drawn_game'] = _response.json()['pc_stat']['drawn_game']
            self.pc_stat['Player_win'] = _response.json()['pc_stat']['Player_win']
            self.pc_stat['Computer_win'] = _response.json()['pc_stat']['Computer_win']
            self.friend_stat['drawn_game'] = _response.json()['friend_stat']['drawn_game']
            self.friend_stat['Player1_win'] = _response.json()['friend_stat']['Player1_win']
            self.friend_stat['Player2_win'] = _response.json()['friend_stat']['Player2_win']
            self.switch_frame(stp.StartPage)
        except FileNotFoundError:
            self.remember_login: bool = False
            import authentification_page as ap
            self.switch_frame(ap.AuthStartPage)

        self._bottom_frame: tk.Frame = tk.Frame(self)
        self._bottom_frame.pack(side='bottom', fill='x', expand=True)
        self._mute_unmute_btn: tk.Button = tk.Button()
        self._mute_unmute_btn_func(self._bottom_frame)

        self._change_language_btn: tk.Button = tk.Button()
        self._change_language_btn_func(self._bottom_frame)

    @staticmethod
    def resource_path(relative_path: str) -> str:
        """
        Method for getting the full path to a file or directory.

        :param relative_path: Relative path to a file or directory
        :type relative_path: class: `str`
        :return: The full path to a file or directory
        :rtype: class: `str`
        """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def _mute_unmute_btn_func(self, frame: tk.Frame) -> None:
        """
        Method of rendering the "Mute/Unmute the background music" button.

        :param frame: Frame for rendering the "Mute/Unmute the background music" button
        :type frame: class: `tkinter.Frame`
        """
        self._mute_unmute_btn = tk.Button(frame, background="white", image=self._unmute_image,
                                          command=self._background_music_mute_unmute)
        self._mute_unmute_btn.pack(side="left", anchor="sw", padx=10, pady=10)

    def _change_language_btn_func(self, frame: tk.Frame) -> None:
        """
        Method of rendering the language change button.

        :param frame: Frame for rendering the language change button
        :type frame: class: `tkinter.Frame`
        """
        self._change_language_btn = tk.Button(frame, background="white", image=self._en_image,
                                              command=self._change_language)
        self._change_language_btn.pack(side="right", anchor="se", padx=10, pady=10)

    def switch_frame(self, frame_class: type) -> None:
        """
        Page change method.

        :param frame_class: The class of any of the game pages
        :type frame_class: class: `type`
        """
        if (self._frame is not None) and (frame_class != gap.FriendGame):
            self.click_music.play()

        if isinstance(self._frame, stp.StartPage):
            self.sign.set("_")
            self.move.set(-1)

        new_frame: Union[stp.StartPage, setp.FriendStartPage, sgp.SearchGamePage,
                         setp.PcStartPage, gap.FriendGame, gap.PcGame] = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def _background_music_mute_unmute(self) -> None:
        """Method with action for the "Mute/Unmute the background music" button."""
        self.click_music.play()
        if not self.mute_flag:
            self.background_music.set_volume(0)
            self._mute_unmute_btn["image"] = self._mute_image
            self.mute_flag = True
        else:
            self.background_music.set_volume(0.3)
            self._mute_unmute_btn["image"] = self._unmute_image
            self.mute_flag = False

    def _change_language(self) -> None:
        """Method with action for the language change button."""
        self.click_music.play()
        if not self.lang_flag:
            self._frame.change_language('ru')
            self._change_language_btn["image"] = self._ru_image
            self.lang_flag = True
        else:
            self._frame.change_language('en')
            self._change_language_btn["image"] = self._en_image
            self.lang_flag = False


if __name__ == "__main__":
    app = App()
    app.mainloop()

    if app.cur_page == 'Search':
        URL = 'http://localhost:5000/reset_search'
        response = requests.get(URL, cookies=app.token)

    if app.cur_page == 'Game_page_pc' and app.now_game:
        app.pc_stat["Computer_win"] += 1

        URL = 'http://localhost:5000/update_computer_statistic'
        headers = {'Content-Type': 'application/json'}
        data = {'games_played': app.pc_stat["Player_win"] + app.pc_stat["Computer_win"] + app.pc_stat["drawn_game"],
                'games_won': app.pc_stat['Player_win'],
                'games_draws': app.pc_stat['drawn_game'], 'games_defeat': app.pc_stat['Computer_win']}
        response = requests.post(URL, headers=headers, data=json.dumps(data), cookies=app.token)
    elif app.cur_page == 'Game_page_fr' and app.now_game:
        app.friend_stat["Player2_win"] += 1

        URL = 'http://localhost:5000/update_friend_statistic'
        headers = {'Content-Type': 'application/json'}
        data = {'games_played': app.friend_stat["Player1_win"] + app.friend_stat["Player2_win"] +
                app.friend_stat["drawn_game"],
                'games_won': app.friend_stat['Player1_win'],
                'games_draws': app.friend_stat['drawn_game'],
                'games_defeat': app.friend_stat['Player2_win']}
        response = requests.post(URL, headers=headers, data=json.dumps(data), cookies=app.token)

        app.sio.emit('reset_game', data={'game_id': app.game_id, 'user_id': app.user_id,
                                         'opponent_id': app.opponent_id})

    if not app.remember_login and app.token is not None:
        URL = 'http://localhost:5000/logout'
        response = requests.get(URL, cookies=app.token)
    try:
        app.sio.disconnect()
    except AttributeError:
        pass
