import tkinter as tk
import random
from typing import Tuple, List, Optional, Dict
import pygame as pg
import setting_page as setp
import tictactoe as ttt


class PcGame(tk.Frame):
    def __init__(self, master: ttt.App) -> None:
        super().__init__(master)

        self.configure(height=650, width=550)
        self.pack_propagate(False)

        self.master: ttt.App

        self._cur_music: pg.mixer.Sound = self.master.win_music

        self.master.cur_page = 'Game_page_pc'

        self._status_msg: str = 'Press "Start" button to start the game'
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
        self._status = tk.Label(self, bg="white", font=self.master.font, text=self._status_msg, width=36, height=2)
        self._status.pack(side="top", pady=15)

    def _create_field(self, frame: tk.Frame) -> List[tk.Button]:
        field = []
        for i in range(9):
            button = tk.Button(frame, text=' ', width=3, height=2, font=('Verdana', 45, 'bold'),
                               background='white', command=lambda square=i: self._click(square),
                               state="disabled")
            button.grid(row=i // 3, column=i % 3, sticky='nsew')
            field.append(button)

        return field

    def _player_sign_lbl(self) -> None:
        tk.Label(self, font=self.master.font, text=self._player_sign_msg).pack(
            side="top", anchor="n", pady=(10, 15))

    def _create_widgets(self) -> None:
        self._player_sign_lbl()

        frame = tk.Frame(self)
        frame.pack(side="top")

        self._field = self._create_field(frame)
        self._status_lbl()
        self._create_return_btn()

    def _create_return_btn(self) -> None:
        self._return_btn = tk.Button(self, bg="white", font=self.master.btn_font, text="Start",
                                     command=self._start_game, width=30)
        self._return_btn.pack(side="top", pady=(0, 15))

    def _begin_cur_sign(self) -> Optional[Tuple[str, str]]:
        if self.master.move.get() == 1:
            return self._user1_sign, self._user1
        elif self.master.move.get() == 2:
            return self._user2_sign, self._user2
        elif self.master.move.get() == 0:
            i = random.randint(0, 1)
            return [self._user1_sign, self._user2_sign][i], [self._user1, self._user2][i]

        return None

    def _sign_choose(self) -> Optional[Tuple[str, str]]:
        if self.master.sign.get() == "R":
            i = random.randint(0, 1)
            return ["X", "O"][i], ["X", "O"][1 - i]
        elif self.master.sign.get() == "X":
            return "X", "O"
        elif self.master.sign.get() == "O":
            return "O", "X"

        return None

    def _switch_frame(self) -> None:
        self.master.switch_frame(setp.PcStartPage)

    def _bind_return_btn(self) -> None:
        self._return_btn_flag = True
        self._return_btn["text"] = "Return to configure page"
        self._return_btn["command"] = self._switch_frame
        self._return_btn["state"] = "disabled"

    @staticmethod
    def _player_name() -> Tuple[str, str]:
        return "Player", "Computer"

    def _precondition(self) -> None:
        for elem in self._field:
            elem["state"] = "normal"
        self._status_msg = "The game has started"
        self._status["text"] = self._status_msg

    def _change_sign_and_status(self) -> None:
        if not self._end_game:
            self._cur_sign, self._cur_player = self._cur_sign_change()

    def _end_game_color(self) -> Tuple[str, str, str]:
        if self._cur_player == "Player":
            return "#90EE90", "#90EE90", "#90EE90"
        else:
            return "#F08080", "#F08080", "#F08080"

    def _set_end_game_music(self) -> None:
        if self._cur_player == "Player":
            self._cur_music = self.master.win_music
        else:
            self._cur_music = self.master.defeat_music

    def _update_statistic(self, flag: bool) -> None:
        if flag:
            self.master.pc_stat[self._cur_player + "_win"] += 1
        else:
            self.master.pc_stat["drawn_game"] += 1

    def _start_game_1(self) -> None:
        self.master.click_music.play()
        self._precondition()
        self._bind_return_btn()

    def _draw_sign(self, square: int) -> None:
        self._field[square]["state"] = "disabled"
        self._field[square]["text"] = self._cur_sign
        self._field[square]["disabledforeground"] = self._color[self._cur_sign]

    def _if_end_game(self) -> None:
        if self._end_game:
            self._cur_music.play()
            for elem in self._free_squares:
                self._field[elem]["state"] = "disabled"
            self._status["text"] = self._status_msg
            self.master.now_game = False
            self._return_btn["state"] = "normal"

    def _click_1(self, square: int) -> None:
        self.master.click_music.play()
        self._draw_sign(square)
        self._free_squares.remove(square)
        self._check_win()
        self._change_sign_and_status()
        self._if_end_game()

    def _set_end_game(self, pos_a: int, pos_b: int, pos_c: int) -> None:
        self._end_game = True
        self._set_end_game_music()
        if self._cur_player == "Computer":
            self._status_msg = "{player} win".format(player=self._cur_player)
        else:
            self._status_msg = "{player} win".format(player=self.master.user)
        self._field[pos_a]["background"], self._field[pos_b]["background"], self._field[pos_c]["background"] = \
            self._end_game_color()

    def _if_drawn_game(self) -> None:
        if not self._free_squares:
            self._end_game = True
            self._is_draw = True
            self._status_msg = "It is a draw"
            self._cur_music = self.master.draw_music
            for elem in self._field:
                elem["background"] = "#F0E68C"
            self._update_statistic(False)

    def _check_win(self) -> None:
        for pos_a, pos_b, pos_c in self._win_pos:
            if (self._field[pos_a]["text"] == self._cur_sign) and (self._field[pos_b]["text"] == self._cur_sign) and \
               (self._field[pos_c]["text"] == self._cur_sign):
                self._set_end_game(pos_a, pos_b, pos_c)
                self._update_statistic(True)
                return

        self._if_drawn_game()

    def _is_win(self, sign: str, field: List[str]) -> bool:
        for pos_a, pos_b, pos_c in self._win_pos:
            if field[pos_a] == sign and field[pos_b] == sign and field[pos_c] == sign:
                return True

        return False

    def _find_best_turn(self, sign: str) -> Optional[int]:
        for i in self._free_squares:
            field = [elem["text"] for elem in self._field]
            field[i] = sign
            result = self._is_win(sign, field)
            if result:
                return i

        return None

    def _default_choice(self) -> Optional[int]:
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
        square = self._find_best_turn(self._user2_sign)
        if square is None:
            square = self._find_best_turn(self._user1_sign)
            if square is None:
                square = self._default_choice()

        self._turn(square)

    def _turn(self, square: int) -> None:
        self._draw_sign(square)
        self._free_squares.remove(square)
        self._check_win()
        self._change_sign_and_status()
        self._if_end_game()

    def _start_game(self) -> None:
        self.master.now_game = True
        self._start_game_1()
        if self._cur_player == "Computer":
            self._computer_turn()

    def _click(self, square: int) -> None:
        self._click_1(square)
        if not self._end_game:
            self._computer_turn()
