import tkinter as tk
import tkinter.font as tkfont
import sys
import os
from pathlib import Path
from typing import Dict
import pygame as pg
from PIL import Image, ImageTk
import authentification_page as ap
import start_page as stp


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Tic-Tac-Toe")
        self.resizable(False, False)

        self._frame = None

        self.font: tkfont.Font = tkfont.Font(size=14, weight="bold", slant="italic")
        self.btn_font: tkfont.Font = tkfont.Font(size=12, weight="normal", slant="italic")

        path1 = self.resource_path("images")
        path2 = self.resource_path("music")

        self.tictactoe_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1,
                                                                                      "TicTacToe.png")).resize(
            (350, 350)))

        self._mute_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1,
                                                                                  "mute.png")).resize((30, 30)))
        self._unmute_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1,
                                                                                    "unmute.png")).resize((30, 30)))

        self.hide_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1, "hide.png")).resize((20, 20)))
        self.show_image: ImageTk.PhotoImage = ImageTk.PhotoImage(Image.open(Path(path1, "show.png")).resize((20, 20)))

        self.friend_stat: Dict[str, int] = {"drawn_game": 0, "Player1_win": 0, "Player2_win": 0}
        self.pc_stat: Dict[str, int] = {"drawn_game": 0, "Player_win": 0, "Computer_win": 0}

        pg.init()
        pg.mixer.init(44100, -16, 1, 512)

        self.background_music: pg.mixer.Sound = pg.mixer.Sound(Path(path2, "music.mp3"))
        self.click_music: pg.mixer.Sound = pg.mixer.Sound(Path(path2, "click.mp3"))
        self.background_music.set_volume(0.3)
        self.click_music.set_volume(1)

        self.sign: tk.StringVar = tk.StringVar()
        self.move: tk.IntVar = tk.IntVar()
        self.sign.set("_")
        self.move.set(-1)

        self.mute_flag: bool = False

        self.background_music.play(-1)

        self._bottom_frame: tk.Frame = tk.Frame(self)
        self._bottom_frame.pack(side='bottom', fill='x', expand=True)
        self._mute_unmute_btn: tk.Button = tk.Button()
        self._mute_unmute_btn_func(self._bottom_frame)

        self.switch_frame(ap.AuthStartPage)

    @staticmethod
    def resource_path(relative_path: str) -> str:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def _mute_unmute_btn_func(self, frame: tk.Frame) -> None:
        self._mute_unmute_btn = tk.Button(frame, background="white", image=self._unmute_image,
                                          command=self._background_music_mute_unmute)
        self._mute_unmute_btn.pack(side="left", anchor="sw", padx=10, pady=10)

    def switch_frame(self, frame_class: type) -> None:
        if self._frame is not None:
            self.click_music.play()

        if isinstance(self._frame, stp.StartPage):
            self.sign.set("_")
            self.move.set(-1)

        new_frame = frame_class(self)

        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def _background_music_mute_unmute(self) -> None:
        self.click_music.play()
        if not self.mute_flag:
            self.background_music.set_volume(0)
            self._mute_unmute_btn["image"] = self._mute_image
            self.mute_flag = True
        else:
            self.background_music.set_volume(0.3)
            self._mute_unmute_btn["image"] = self._unmute_image
            self.mute_flag = False


if __name__ == "__main__":
    app = App()
    app.mainloop()
