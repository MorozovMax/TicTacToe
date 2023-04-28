"""
A module with a parent class of game settings page, as well as classes of online game
settings page and computer game settings page inherited from it.
"""

import tkinter as tk
import os
import sys
import json
import gettext
from typing import Callable
import requests
import start_page as stp
import game_page as gap
import search_game_page as sgp


translation = gettext.translation('tictactoe',
                                  os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),
                                               'locale'),
                                  fallback=True)


class BaseStartPage(tk.Frame):
    """
    The class of the registration page.

    :param master: An instance of the main class of the game application
    :type master: class: `tictactoe.App`
    """

    def __init__(self, master) -> None:
        """Constructor method."""
        super().__init__(master)

        self.configure(height=280, width=800)
        self.pack_propagate(False)

        if not self.master.lang_flag:
            self._: Callable = lambda s: s
        else:
            self._: Callable = translation.gettext

        self.label1: tk.Label = tk.Label()
        self.statistics: tk.LabelFrame = tk.LabelFrame()
        self.statistics1: tk.Label = tk.Label()
        self.statistics2: tk.Label = tk.Label()
        self.statistics3: tk.Label = tk.Label()
        self.statistics4: tk.Label = tk.Label()
        self.button1: tk.Button = tk.Button()
        self.button2: tk.Button = tk.Button()
        self.step_choice: tk.LabelFrame = tk.LabelFrame()
        self.step_choice1: tk.Radiobutton = tk.Radiobutton()
        self.step_choice2: tk.Radiobutton = tk.Radiobutton()
        self.step_choice3: tk.Radiobutton = tk.Radiobutton()
        self.sign_selection: tk.LabelFrame = tk.LabelFrame()
        self.sign_selection1: tk.Radiobutton = tk.Radiobutton()
        self.sign_selection2: tk.Radiobutton = tk.Radiobutton()
        self.sign_selection3: tk.Radiobutton = tk.Radiobutton()

        self._create_widgets()

    def _sound(self) -> None:
        """Method for playing the sound of pressing the button."""
        self.master.click_music.play(0)

    def _choose_move_widget(self, frame: tk.Frame) -> None:
        """
        A method for drawing a named frame with a choice of the sequence of the move.

        :param frame: A frame for drawing a named frame with a choice of the sequence of the move
        :type frame: class: `tkinter.Frame`
        """
        self.step_choice = tk.LabelFrame(frame, font=self.master.font,
                                         text=self._(" Choosing a move "), labelanchor="n")
        self.step_choice.pack(side="left", padx=(0, 12), anchor="nw")

        if self.master.move.get() == -1:
            self.master.move.set(0)
        else:
            self.master.move.set(self.master.move.get())

        self.step_choice1 = tk.Radiobutton(self.step_choice, font=self.master.btn_font, bg="white",
                                           text=self._("Randomly"), variable=self.master.move,
                                           value=0, width=15, command=self._sound)
        self.step_choice1.pack(side="top", pady=(8, 4), padx=5)

        self.step_choice2 = tk.Radiobutton(self.step_choice, font=self.master.btn_font, bg="white",
                                           text=self._("First"), variable=self.master.move,
                                           value=1, width=15, command=self._sound)
        self.step_choice2.pack(side="top", padx=5)

        self.step_choice3 = tk.Radiobutton(self.step_choice, font=self.master.btn_font, bg="white",
                                           text=self._("Second"), variable=self.master.move,
                                           value=2, width=15, command=self._sound)
        self.step_choice3.pack(side="top", pady=(4, 14), padx=5)

    def _sign_selection(self, frame: tk.Frame) -> None:
        """
        Method for drawing a named frame with a sign selection.

        :param frame: Frame for drawing a named frame with a choice of sign
        :type frame: class: `tkinter.Frame`
        """
        self.sign_selection = tk.LabelFrame(frame, font=self.master.font,
                                            text=self._(" Sign selection "), labelanchor="n")
        self.sign_selection.pack(side="left", padx=(0, 12), anchor="nw")

        if self.master.sign.get() == "_":
            self.master.sign.set("R")
        else:
            self.master.sign.set(self.master.sign.get())

        self.sign_selection1 = tk.Radiobutton(self.sign_selection, font=self.master.btn_font, bg="white",
                                              text=self._("Randomly"), variable=self.master.sign, value="R", width=15,
                                              command=self._sound)
        self.sign_selection1.pack(side="top", pady=(8, 4), padx=5)

        self.sign_selection2 = tk.Radiobutton(self.sign_selection, font=self.master.btn_font, bg="white",
                                              text=self._('Your sign - "X"'), variable=self.master.sign, value="X",
                                              width=15, command=self._sound)
        self.sign_selection2.pack(side="top", padx=5)

        self.sign_selection3 = tk.Radiobutton(self.sign_selection, font=self.master.btn_font, bg="white",
                                              text=self._('Your sign - "O"'), variable=self.master.sign, value="O",
                                              width=15, command=self._sound)
        self.sign_selection3.pack(side="top", pady=(4, 14), padx=5)

    def _game_type(self) -> None:
        """Method for drawing a label with a game type."""
        pass

    def _start_and_return_btn(self, frame: tk.Frame) -> None:
        """
        A method for drawing the start game and return to the start page buttons.

        :param frame: Frame for drawing the start game and return to the start page buttons
        :type frame: class: `tkinter.Frame`
        """
        pass

    def _statistic_widget(self, frame: tk.Frame) -> None:
        """
        Method for rendering a label frame with statistics.

        :param frame: Frame for drawing a label frame with statistics
        :type frame: class: `tkinter.Frame`
        """
        pass

    def _create_widgets(self) -> None:
        """The method of rendering widgets of the game settings page."""
        self._game_type()

        frame1 = tk.Frame(self)
        frame1.pack(side="top", pady=15)

        self._statistic_widget(frame1)
        self._choose_move_widget(frame1)
        self._sign_selection(frame1)

        frame2 = tk.Frame(self)
        frame2.pack(side="top")

        self._start_and_return_btn(frame2)


class FriendStartPage(BaseStartPage):
    """
    The class of the registration page.

    :param master: An instance of the main class of the game application
    :type master: class: `tictactoe.App`
    """

    def __init__(self, master) -> None:
        """Constructor method."""
        super().__init__(master)

    def _game_type(self) -> None:
        """Method for drawing a label with the online game type."""
        self.label1 = tk.Label(self, font=self.master.font, text=self._("Online game"))
        self.label1.pack(side="top", pady=(10, 0))

    def search_game(self) -> None:
        """A method with an action for the "Search the game" button."""
        url = 'http://localhost:5000/join_queue'
        headers = {'Content-Type': 'application/json'}
        data = {'sign': self.master.sign.get(), 'turn': str(self.master.move.get())}
        requests.post(url, headers=headers, data=json.dumps(data), cookies=self.master.token)
        self.master.switch_frame(sgp.SearchGamePage)

    def _statistic_widget(self, frame: tk.Frame) -> None:
        """
        Method for rendering a label frame with online game statistics.

        :param frame: Frame for drawing a label frame with online game statistics
        :type frame: class: `tkinter.Frame`
        """
        self.statistics = tk.LabelFrame(frame, font=self.master.font, text=" Game statistic ", labelanchor="n")
        self.statistics.pack(side="left", padx=12, anchor="nw")
        self.statistics1 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text=self._("Number of played games - {}").format(self.master.friend_stat[
                                                                                          "Player1_win"] +
                                                                                      self.master.friend_stat[
                                                                                          "Player2_win"] +
                                                                                      self.master.friend_stat[
                                                                                          "drawn_game"]),
                                    width=30)
        self.statistics1.pack(side="top", pady=(5, 0), padx=5)

        self.statistics2 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text=self._("Number of user wins - {}").format(self.master.friend_stat[
                                                                                       "Player1_win"]),
                                    width=30)
        self.statistics2.pack(side="top", padx=5)

        self.statistics3 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text=self._("Number of user defeats - {}").format(self.master.friend_stat[
                                                                                          "Player2_win"]),
                                    width=30)
        self.statistics3.pack(side="top", padx=5)

        self.statistics4 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text=self._("Number of draws - {}").format(self.master.friend_stat["drawn_game"]),
                                    width=30)
        self.statistics4.pack(side="top", pady=(0, 8), padx=5)

    def _start_and_return_btn(self, frame: tk.Frame) -> None:
        """
        A method for drawing the search the game and return to the start page buttons.

        :param frame: Frame for drawing the search the game and return to the start page buttons
        :type frame: class: `tkinter.Frame`
        """
        self.button1 = tk.Button(frame, bg="white", font=self.master.btn_font, text="Search the game",
                                 command=self.search_game, width=30)
        self.button1.pack(side="top", pady=(0, 5))

        self.button2 = tk.Button(frame, bg="white", font=self.master.btn_font, text=self._("Return to start page"),
                                 command=lambda: self.master.switch_frame(stp.StartPage), width=30)
        self.button2.pack(side="top")

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
        self.label1.config(text=self._("Online game"))
        self.statistics.config(text=self._(" Game statistic "))
        self.statistics1.config(text=self._("Number of played games - {}").format(self.master.friend_stat[
                                                                                      "Player1_win"] +
                                                                                  self.master.friend_stat[
                                                                                      "Player2_win"] +
                                                                                  self.master.friend_stat[
                                                                                      "drawn_game"]))
        self.statistics2.config(text=self._("Number of user wins - {}").format(self.master.friend_stat["Player1_win"]))
        self.statistics3.config(text=self._("Number of user defeats - {}").format(self.master.friend_stat[
                                                                                      "Player2_win"]))
        self.statistics4.config(text=self._("Number of draws - {}").format(self.master.friend_stat["drawn_game"]))
        self.button1.config(text=self._("Search the game"))
        self.button2.config(text=self._("Return to start page"))
        self.step_choice.config(text=self._(" Choosing a move "))
        self.step_choice1.config(text=self._('Randomly'))
        self.step_choice2.config(text=self._("First"))
        self.step_choice3.config(text=self._("Second"))
        self.sign_selection.config(text=self._(" Sign selection "))
        self.sign_selection1.config(text=self._('Randomly'))
        self.sign_selection2.config(text=self._('Your sign - "X"'))
        self.sign_selection3.config(text=self._('Your sign - "O"'))


class PcStartPage(BaseStartPage):
    """
    The class of the registration page.

    :param master: An instance of the main class of the game application
    :type master: class: `tictactoe.App`
    """

    def __init__(self, master) -> None:
        """Constructor method."""
        super().__init__(master)

    def _game_type(self) -> None:
        """Method for drawing a label with the computer game type."""
        self.label1 = tk.Label(self, font=self.master.font, text=self._("Game with computer"))
        self.label1.pack(side="top", pady=(10, 0))

    def _statistic_widget(self, frame: tk.Frame) -> None:
        """
        Method for rendering a label frame with computer game statistics.

        :param frame: Frame for drawing a label frame with computer game statistics
        :type frame: class: `tkinter.Frame`
        """
        self.statistics = tk.LabelFrame(frame, font=self.master.font, text=" Game statistic ", labelanchor="n")
        self.statistics.pack(side="left", padx=12, anchor="nw")
        self.statistics1 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text=self._("Number of played games - {}").format(self.master.pc_stat[
                                                                                          "Player_win"] +
                                                                                      self.master.pc_stat[
                                                                                          "Computer_win"] +
                                                                                      self.master.pc_stat[
                                                                                          "drawn_game"]),
                                    width=30)
        self.statistics1.pack(side="top", pady=(5, 0), padx=5)

        self.statistics2 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text=self._("Number of user wins - {}").format(self.master.pc_stat["Player_win"]),
                                    width=30)
        self.statistics2.pack(side="top", padx=5)

        self.statistics3 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text=self._("Number of user defeats - {}").format(self.master.pc_stat[
                                                                                          "Computer_win"]),
                                    width=30)
        self.statistics3.pack(side="top", padx=5)

        self.statistics4 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text=self._("Number of draws - {}").format(self.master.pc_stat["drawn_game"]),
                                    width=30)
        self.statistics4.pack(side="top", pady=(0, 8), padx=5)

    def _start_and_return_btn(self, frame: tk.Frame) -> None:
        """
        A method for drawing the start computer game and return to the start page buttons.

        :param frame: Frame for drawing the start computer game and return to the start page buttons
        :type frame: class: `tkinter.Frame`
        """
        self.button1 = tk.Button(frame, bg="white", font=self.master.btn_font, text="Start the game",
                                 command=lambda: self.master.switch_frame(gap.PcGame), width=30)
        self.button1.pack(side="top", pady=(0, 5))

        self.button2 = tk.Button(frame, bg="white", font=self.master.btn_font, text=self._("Return to start page"),
                                 command=lambda: self.master.switch_frame(stp.StartPage), width=30)
        self.button2.pack(side="top")

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
        self.label1.config(text=self._("Game with computer"))
        self.statistics.config(text=self._(" Game statistic "))
        self.statistics1.config(text=self._("Number of played games - {}").format(self.master.friend_stat[
                                                                                      "Player1_win"] +
                                                                                  self.master.friend_stat[
                                                                                      "Player2_win"] +
                                                                                  self.master.friend_stat[
                                                                                      "drawn_game"]))
        self.statistics2.config(text=self._("Number of user wins - {}").format(self.master.friend_stat["Player1_win"]))
        self.statistics3.config(
            text=self._("Number of user defeats - {}").format(self.master.friend_stat["Player2_win"]))
        self.statistics4.config(text=self._("Number of draws - {}").format(self.master.friend_stat["drawn_game"]))
        self.button1.config(text=self._("Start the game"))
        self.button2.config(text=self._("Return to start page"))
        self.step_choice.config(text=self._(" Choosing a move "))
        self.step_choice1.config(text=self._('Randomly'))
        self.step_choice2.config(text=self._("First"))
        self.step_choice3.config(text=self._("Second"))
        self.sign_selection.config(text=self._(" Sign selection "))
        self.sign_selection1.config(text=self._('Randomly'))
        self.sign_selection2.config(text=self._('Your sign - "X"'))
        self.sign_selection3.config(text=self._('Your sign - "O"'))
