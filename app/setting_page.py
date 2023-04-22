import tkinter as tk
import start_page as stp
import tictactoe as ttt
import game_page as gap


class BaseStartPage(tk.Frame):
    def __init__(self, master: ttt.App) -> None:
        super().__init__(master)

        self.master: ttt.App

        self.configure(height=280, width=800)
        self.pack_propagate(False)

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
        self.master.click_music.play(0)

    def _choose_move_widget(self, frame: tk.Frame) -> None:
        self.step_choice = tk.LabelFrame(frame, font=self.master.font,
                                         text=" Choosing a move ", labelanchor="n")
        self.step_choice.pack(side="left", padx=(0, 12), anchor="nw")

        if self.master.move.get() == -1:
            self.master.move.set(0)
        else:
            self.master.move.set(self.master.move.get())

        self.step_choice1 = tk.Radiobutton(self.step_choice, font=self.master.btn_font, bg="white",
                                           text="Randomly", variable=self.master.move,
                                           value=0, width=15, command=self._sound)
        self.step_choice1.pack(side="top", pady=(8, 4), padx=5)

        self.step_choice2 = tk.Radiobutton(self.step_choice, font=self.master.btn_font, bg="white",
                                           text="First", variable=self.master.move,
                                           value=1, width=15, command=self._sound)
        self.step_choice2.pack(side="top", padx=5)

        self.step_choice3 = tk.Radiobutton(self.step_choice, font=self.master.btn_font, bg="white",
                                           text="Second", variable=self.master.move,
                                           value=2, width=15, command=self._sound)
        self.step_choice3.pack(side="top", pady=(4, 14), padx=5)

    def _sign_selection(self, frame: tk.Frame) -> None:
        self.sign_selection = tk.LabelFrame(frame, font=self.master.font,
                                            text=" Sign selection ", labelanchor="n")
        self.sign_selection.pack(side="left", padx=(0, 12), anchor="nw")

        if self.master.sign.get() == "_":
            self.master.sign.set("R")
        else:
            self.master.sign.set(self.master.sign.get())

        self.sign_selection1 = tk.Radiobutton(self.sign_selection, font=self.master.btn_font, bg="white",
                                              text="Randomly", variable=self.master.sign, value="R", width=15,
                                              command=self._sound)
        self.sign_selection1.pack(side="top", pady=(8, 4), padx=5)

        self.sign_selection2 = tk.Radiobutton(self.sign_selection, font=self.master.btn_font, bg="white",
                                              text='Your sign - "X"', variable=self.master.sign, value="X",
                                              width=15, command=self._sound)
        self.sign_selection2.pack(side="top", padx=5)

        self.sign_selection3 = tk.Radiobutton(self.sign_selection, font=self.master.btn_font, bg="white",
                                              text='Your sign - "O"', variable=self.master.sign, value="O",
                                              width=15, command=self._sound)
        self.sign_selection3.pack(side="top", pady=(4, 14), padx=5)

    def _game_type(self) -> None:
        pass

    def _start_and_return_btn(self, frame: tk.Frame) -> None:
        pass

    def _statistic_widget(self, frame: tk.Frame) -> None:
        pass

    def _create_widgets(self) -> None:
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
    def __init__(self, master: ttt.App) -> None:
        super().__init__(master)

    def _game_type(self) -> None:
        self.label1 = tk.Label(self, font=self.master.font, text="Online game")
        self.label1.pack(side="top", pady=(10, 0))

    def search_game(self) -> None:
        pass

    def _statistic_widget(self, frame: tk.Frame) -> None:
        self.statistics = tk.LabelFrame(frame, font=self.master.font, text=" Game statistic ", labelanchor="n")
        self.statistics.pack(side="left", padx=12, anchor="nw")
        self.statistics1 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text="Number of played games - {}".format(self.master.friend_stat[
                                                                                          "Player1_win"] +
                                                                                      self.master.friend_stat[
                                                                                          "Player2_win"] +
                                                                                      self.master.friend_stat[
                                                                                          "drawn_game"]),
                                    width=30)
        self.statistics1.pack(side="top", pady=(5, 0), padx=5)

        self.statistics2 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text="Number of user wins - {}".format(self.master.friend_stat[
                                                                                       "Player1_win"]),
                                    width=30)
        self.statistics2.pack(side="top", padx=5)

        self.statistics3 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text="Number of user defeats - {}".format(self.master.friend_stat[
                                                                                          "Player2_win"]),
                                    width=30)
        self.statistics3.pack(side="top", padx=5)

        self.statistics4 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text="Number of draws - {}".format(self.master.friend_stat["drawn_game"]),
                                    width=30)
        self.statistics4.pack(side="top", pady=(0, 8), padx=5)

    def _start_and_return_btn(self, frame: tk.Frame) -> None:
        self.button1 = tk.Button(frame, bg="white", font=self.master.btn_font, text="Search the game",
                                 command=self.search_game, width=30)
        self.button1.pack(side="top", pady=(0, 5))

        self.button2 = tk.Button(frame, bg="white", font=self.master.btn_font, text="Return to start page",
                                 command=lambda: self.master.switch_frame(stp.StartPage), width=30)
        self.button2.pack(side="top")


class PcStartPage(BaseStartPage):
    def __init__(self, master: ttt.App) -> None:
        super().__init__(master)

    def _game_type(self) -> None:
        self.label1 = tk.Label(self, font=self.master.font, text="Game with computer")
        self.label1.pack(side="top", pady=(10, 0))

    def _statistic_widget(self, frame: tk.Frame) -> None:
        self.statistics = tk.LabelFrame(frame, font=self.master.font, text=" Game statistic ", labelanchor="n")
        self.statistics.pack(side="left", padx=12, anchor="nw")
        self.statistics1 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text="Number of played games - {}".format(self.master.pc_stat[
                                                                                          "Player_win"] +
                                                                                      self.master.pc_stat[
                                                                                          "Computer_win"] +
                                                                                      self.master.pc_stat[
                                                                                          "drawn_game"]),
                                    width=30)
        self.statistics1.pack(side="top", pady=(5, 0), padx=5)

        self.statistics2 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text="Number of user wins - {}".format(self.master.pc_stat["Player_win"]),
                                    width=30)
        self.statistics2.pack(side="top", padx=5)

        self.statistics3 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text="Number of user defeats - {}".format(self.master.pc_stat[
                                                                                          "Computer_win"]),
                                    width=30)
        self.statistics3.pack(side="top", padx=5)

        self.statistics4 = tk.Label(self.statistics, font=self.master.btn_font, bg="white",
                                    text="Number of draws - {}".format(self.master.pc_stat["drawn_game"]),
                                    width=30)
        self.statistics4.pack(side="top", pady=(0, 8), padx=5)

    def _start_and_return_btn(self, frame: tk.Frame) -> None:
        self.button1 = tk.Button(frame, bg="white", font=self.master.btn_font, text="Start the game",
                                 command=lambda: self.master.switch_frame(gap.PcGame), width=30)
        self.button1.pack(side="top", pady=(0, 5))

        self.button2 = tk.Button(frame, bg="white", font=self.master.btn_font, text="Return to start page",
                                 command=lambda: self.master.switch_frame(stp.StartPage), width=30)
        self.button2.pack(side="top")
