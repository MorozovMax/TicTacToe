import tkinter as tk
import tkinter.font as tkfont
import threading
import setting_page as setp
import tictactoe as ttt


class TimeCounter(tk.Label):
    def __init__(self, parent: 'SearchGamePage', font: tkfont.Font, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.font: tkfont.Font = font
        self.total_seconds: int = 0
        self.update_text()

    def start(self) -> None:
        self.total_seconds = 0
        self.update_text()
        self.run()

    def run(self) -> None:
        self.total_seconds += 1
        self.update_text()
        self.after(1000, self.run)

    def update_text(self) -> None:
        minutes, seconds = divmod(self.total_seconds, 60)
        self.config(text=f"{minutes:02d}:{seconds:02d}", font=self.font)


class CircularWaitingIndicator(tk.Canvas):
    def __init__(self, parent: 'SearchGamePage', width: int = 80, height: int = 80, color: str = 'blue',
                 thickness: int = 5, speed: int = 5) -> None:
        super().__init__(parent, width=90, height=90)
        self.color: str = color
        self.thickness: int = thickness
        self.speed: int = speed

        self.create_oval(10, 10, width, height, outline=color, width=thickness)
        self.arc: int = self.create_arc(10, 10, width, height, start=90, extent=0, outline=color, width=thickness)

        self.update_animation()

    def update_animation(self) -> None:
        extent = (float(self.itemcget(self.arc, 'extent')) - self.speed) % 360
        self.itemconfigure(self.arc, extent=extent)
        self.after(50, self.update_animation)


class SearchGamePage(tk.Frame):
    def __init__(self, master: ttt.App) -> None:
        super().__init__(master)

        self.master: ttt.App

        self.master.cur_page = 'Search'

        self.reset: bool = False

        self.configure(height=320, width=450)
        self.pack_propagate(False)

        self.warning_message: tk.Label = tk.Label()
        self.button: tk.Button = tk.Button()

        self.label1: tk.Label = tk.Label()

        self._create_widgets()

        self.thread: threading.Thread = threading.Thread(target=self.is_searched, daemon=True)
        self.thread.start()

    def is_searched(self) -> None:
        pass

    def reset_search(self) -> None:
        self.reset = True
        self.master.switch_frame(setp.FriendStartPage)

    def _create_widgets(self) -> None:
        self.label1 = tk.Label(self, font=self.master.font, text='The game is being searched for')
        self.label1.pack(side="top", pady=(15, 30))

        indicator = CircularWaitingIndicator(self)
        indicator.pack(side="top", pady=(0, 30))

        counter = TimeCounter(self, self.master.font)
        counter.pack(side="top", pady=(0, 20))
        counter.start()

        frame = tk.Frame(self)
        frame.pack(side="top", pady=(0, 20))

        self.warning_message = tk.Label(frame, font=self.master.font, text='', fg='green')
        self.warning_message.pack()

        self.button = tk.Button(self, bg="white", font=self.master.btn_font, text="Reset search", width=30,
                                command=self.reset_search)
        self.button.pack(side='top')
