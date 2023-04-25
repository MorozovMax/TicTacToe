"""A module with the class of the game's home page, where you can choose the game mode or log out of your account."""

import tkinter as tk
import os
import requests
import setting_page as setp
import authentification_page as ap


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

        self.label: tk.Label = tk.Label()
        self.button1: tk.Button = tk.Button()
        self.button2: tk.Button = tk.Button()
        self.button3: tk.Button = tk.Button()

        self._create_widgets()

    def _create_widgets(self) -> None:
        """The method of rendering widgets of the home page."""
        self.label = tk.Label(self, font=self.master.font,
                              text='Player is {user}'.format(user=self.master.user))
        self.label.pack(side="top", pady=(15, 25))

        self._create_image()

        self.button1 = tk.Button(self, bg="white", font=self.master.btn_font, text="Online game", width=30,
                                 command=lambda: self.master.switch_frame(setp.FriendStartPage))
        self.button1.pack(side="top", pady=(40, 5))

        self.button2 = tk.Button(self, bg="white", font=self.master.btn_font, text="Play with the computer",
                                 width=30, command=lambda: self.master.switch_frame(setp.PcStartPage))
        self.button2.pack(side="top", pady=(0, 5))

        self.button3 = tk.Button(self, bg="white", font=self.master.btn_font, text="Log Out", width=30,
                                 command=self._logout)
        self.button3.pack(side='top')

    def _logout(self) -> None:
        """A method with an action for the "Log out" button."""
        url = 'http://localhost:5000/logout'
        requests.get(url, cookies=self.master.token)
        self.master.token = None
        try:
            os.remove(self.master.resource_path('token.pickle'))
        except OSError:
            pass
        self.master.switch_frame(ap.AuthStartPage)

    def _create_image(self) -> None:
        """The method of drawing the image for the start page."""
        canvas = tk.Canvas(self, bg="white", height=400, width=400)
        canvas.create_image(25, 25, anchor="nw", image=self.master.tictactoe_image)
        canvas.pack(side="top")
