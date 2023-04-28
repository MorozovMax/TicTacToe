"""A module with the class of the game's home page, where you can choose the game mode or log out of your account."""

import tkinter as tk
import os
import sys
import gettext
from typing import Callable
import requests
import setting_page as setp
import authentification_page as ap


translation = gettext.translation('tictactoe',
                                  os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
                                               'locale'),
                                  fallback=True)


class StartPage(tk.Frame):
    """
    The class of the game's home page, where you can choose the game mode or log out of your account.

    :param master: An instance of the main class of the game application
    :type master: class: `tictactoe.App`
    """

    def __init__(self, master) -> None:
        """The constructor method."""
        super().__init__(master)

        self.configure(height=650, width=550)
        self.pack_propagate(False)

        if not self.master.lang_flag:
            self._: Callable = lambda s: s
        else:
            self._: Callable = translation.gettext

        self.label: tk.Label = tk.Label()
        self.button1: tk.Button = tk.Button()
        self.button2: tk.Button = tk.Button()
        self.button3: tk.Button = tk.Button()

        self._create_widgets()

    def _create_widgets(self) -> None:
        """The method of rendering widgets of the home page."""
        self.label = tk.Label(self, font=self.master.font,
                              text=self._('Player is {user}').format(user=self.master.user))
        self.label.pack(side="top", pady=(15, 25))

        self._create_image()

        self.button1 = tk.Button(self, bg="white", font=self.master.btn_font, text=self._("Online game"), width=30,
                                 command=lambda: self.master.switch_frame(setp.FriendStartPage))
        self.button1.pack(side="top", pady=(40, 5))

        self.button2 = tk.Button(self, bg="white", font=self.master.btn_font, text=self._("Play with the computer"),
                                 width=30, command=lambda: self.master.switch_frame(setp.PcStartPage))
        self.button2.pack(side="top", pady=(0, 5))

        self.button3 = tk.Button(self, bg="white", font=self.master.btn_font, text=self._("Log Out"), width=30,
                                 command=self._logout)
        self.button3.pack(side='top')

    def _logout(self) -> None:
        """A method with an action for the "Log out" button."""
        url = 'http://localhost:5000/logout'
        requests.get(url, cookies=self.master.token)
        self.master.token = None
        try:
            os.remove('token.pickle')
        except OSError:
            pass
        self.master.switch_frame(ap.AuthStartPage)

    def _create_image(self) -> None:
        """The method of drawing the image for the start page."""
        canvas = tk.Canvas(self, bg="white", height=400, width=400)
        canvas.create_image(25, 25, anchor="nw", image=self.master.tictactoe_image)
        canvas.pack(side="top")

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
        self.label.config(text=self._('Player is {user}').format(user=self.master.user))
        self.button1.config(text=self._("Online game"))
        self.button2.config(text=self._("Play with the computer"))
        self.button3.config(text=self._("Log Out"))
