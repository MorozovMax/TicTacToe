import tkinter as tk
import json
import pickle
import requests
import start_page as stp


class AuthStartPage(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.configure(height=600, width=550)
        self.pack_propagate(False)

        self.label: tk.Label = tk.Label()
        self.button1: tk.Button = tk.Button()
        self.button2: tk.Button = tk.Button()

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.label = tk.Label(self, font=self.master.font, text='Welcome to the "Tic-Tac-Toe" game!')
        self.label.pack(side="top", pady=(15, 25))

        self._create_image()

        self.button1 = tk.Button(self, bg="white", font=self.master.btn_font, text="Register", width=30,
                                 command=lambda: self.master.switch_frame(RegisterPage))
        self.button1.pack(side="top", pady=(40, 5))

        self.button2 = tk.Button(self, bg="white", font=self.master.btn_font, text="Log in", width=30,
                                 command=lambda: self.master.switch_frame(LoginPage))
        self.button2.pack(side="top")

    def _create_image(self) -> None:
        canvas = tk.Canvas(self, bg="white", height=400, width=400)
        canvas.create_image(25, 25, anchor="nw", image=self.master.tictactoe_image)
        canvas.pack(side="top")


class RegisterPage(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.configure(height=280, width=800)
        self.pack_propagate(False)

        self.label1: tk.Label = tk.Label()
        self.label2: tk.Label = tk.Label()
        self.label3: tk.Label = tk.Label()
        self.button1: tk.Button = tk.Button()
        self.warning_message: tk.Label = tk.Label()
        self.register_button: tk.Button = tk.Button()

        self._create_widgets()

    def toggle_password_visibility(self, passwd_entry: tk.Entry, button: tk.Button) -> None:
        self.master.click_music.play()
        current_value = passwd_entry["show"]
        if current_value == "*":
            passwd_entry.config(show="")
            button["image"] = self.master.hide_image
        else:
            passwd_entry.config(show="*")
            button["image"] = self.master.show_image

    def register(self, username: str, password: str, label: tk.Label, frame: tk.Frame) -> None:
        if username == '' or password == '':
            self.master.click_music.play()
            label.config(text='Username and password can`t be empty')
            frame.after(1000, lambda: label.config(text=""))
            return

        url = 'http://localhost:5000/register'
        headers = {'Content-Type': 'application/json'}
        data = {'username': username, 'password': password}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.json()['message'] == 'Username already exists':
            self.master.click_music.play()
            label.config(text='Username "{username}" already exists'.format(username=username))
            frame.after(1000, lambda: label.config(text=""))
        else:
            self.master.switch_frame(AuthStartPage)

    def _create_widgets(self) -> None:
        frame0 = tk.Frame(self)
        frame0.pack(side="top", pady=(15, 10))

        self.label1 = tk.Label(frame0, font=self.master.font, text="Register page")
        self.label1.pack()

        frame1 = tk.Frame(self)
        frame1.pack(side="top", pady=(15, 5))

        self.label2 = tk.Label(frame1, font=self.master.font, text="Username")
        self.label2.pack(side='left', padx=(0, 10))

        username_entry = tk.Entry(frame1, font=self.master.btn_font, width=60)
        username_entry.pack(side='left')

        frame2 = tk.Frame(self)
        frame2.pack(side="top", pady=(0, 15))

        self.label3 = tk.Label(frame2, font=self.master.font, text="Password")
        self.label3.pack(side='left', padx=(0, 10))
        password_entry = tk.Entry(frame2, font=self.master.btn_font, show="*", width=57)
        password_entry.pack(side='left')

        view_password_button = tk.Button(frame2, bg='white', image=self.master.show_image,
                                         command=lambda: self.toggle_password_visibility(password_entry,
                                                                                         view_password_button))
        view_password_button.pack(side='left')

        frame3 = tk.Frame(self)
        frame3.pack(side="top", pady=(0, 15))

        self.warning_message = tk.Label(frame3, font=self.master.font, text='', fg='red')
        self.warning_message.pack()

        frame4 = tk.Frame(self)
        frame4.pack(side="top", pady=(0, 5))

        self.register_button = tk.Button(frame4, bg="white", width=30, font=self.master.btn_font,
                                         text="Register",
                                         command=lambda: self.register(username_entry.get(),
                                                                       password_entry.get(),
                                                                       self.warning_message, frame3))
        self.register_button.pack()

        self.button1 = tk.Button(self, bg="white", font=self.master.btn_font,
                                 text="Return to authorization page",
                                 command=lambda: self.master.switch_frame(AuthStartPage), width=30)
        self.button1.pack(side="top", pady=(0, 0))


class LoginPage(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.configure(height=300, width=800)
        self.pack_propagate(False)

        self.label1: tk.Label = tk.Label()
        self.label2: tk.Label = tk.Label()
        self.label3: tk.Label = tk.Label()
        self.button1: tk.Button = tk.Button()
        self.warning_message: tk.Label = tk.Label()
        self.register_button: tk.Button = tk.Button()
        self.remember_me_checkbox: tk.Checkbutton = tk.Checkbutton()

        self._create_widgets()

    def toggle_password_visibility(self, passwd_entry: tk.Entry, button: tk.Button) -> None:
        self.master.click_music.play()
        current_value = passwd_entry["show"]
        if current_value == "*":
            passwd_entry.config(show="")
            button["image"] = self.master.hide_image
        else:
            passwd_entry.config(show="*")
            button["image"] = self.master.show_image

    def login(self, username: str, password: str, remember_me: tk.BooleanVar, label: tk.Label,
              frame: tk.Frame) -> None:
        if username == '' or password == '':
            self.master.click_music.play()
            label.config(text='Username and password can`t be empty')
            frame.after(1000, lambda: label.config(text=""))
            return

        url = 'http://localhost:5000/login'
        headers = {'Content-Type': 'application/json'}
        data = {'username': username, 'password': password}
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.json()['message'] == 'Invalid username or password':
            self.master.click_music.play()
            label.config(text='Invalid username or password')
            frame.after(1000, lambda: label.config(text=""))
        elif response.json()['message'] == 'Error':
            self.master.click_music.play()
            label.config(text='{username} already logged in'.format(username=username))
            frame.after(1000, lambda: label.config(text=""))
        else:
            self.master.token = response.cookies
            self.master.user_id = response.json()['user_id']
            if remember_me.get():
                with open(self.master.resource_path('token.pickle', 'wb')) as file:
                    pickle.dump(self.master.token, file)

                self.master.remember_login = True

            self.master.user = username
            self.master.pc_stat['drawn_game'] = response.json()['pc_stat']['drawn_game']
            self.master.pc_stat['Player_win'] = response.json()['pc_stat']['Player_win']
            self.master.pc_stat['Computer_win'] = response.json()['pc_stat']['Computer_win']
            self.master.friend_stat['drawn_game'] = response.json()['friend_stat']['drawn_game']
            self.master.friend_stat['Player1_win'] = response.json()['friend_stat']['Player1_win']
            self.master.friend_stat['Player2_win'] = response.json()['friend_stat']['Player2_win']
            self.master.switch_frame(stp.StartPage)

    def _create_widgets(self) -> None:
        frame0 = tk.Frame(self)
        frame0.pack(side="top", pady=(15, 10))

        self.label1 = tk.Label(frame0, font=self.master.font, text="Log in page")
        self.label1.pack()

        frame1 = tk.Frame(self)
        frame1.pack(side="top", pady=(15, 5))

        self.label2 = tk.Label(frame1, font=self.master.font, text="Username")
        self.label2.pack(side='left', padx=(0, 10))

        username_entry = tk.Entry(frame1, font=self.master.btn_font, width=60)
        username_entry.pack(side='left')

        frame2 = tk.Frame(self)
        frame2.pack(side="top", pady=(0, 5))

        self.label3 = tk.Label(frame2, font=self.master.font, text="Password")
        self.label3.pack(side='left', padx=(0, 10))

        password_entry = tk.Entry(frame2, font=self.master.btn_font, show="*", width=57)
        password_entry.pack(side='left')

        view_password_button = tk.Button(frame2, bg='white', image=self.master.show_image,
                                         command=lambda: self.toggle_password_visibility(password_entry,
                                                                                         view_password_button))
        view_password_button.pack(side='left')

        frame4 = tk.Frame(self)
        frame4.pack(side="top", pady=(0, 15))

        remember_me_var = tk.BooleanVar()
        self.remember_me_checkbox = tk.Checkbutton(frame4, font=self.master.btn_font, text="Remember Me",
                                                   variable=remember_me_var, command=self.master.click_music.play)
        self.remember_me_checkbox.pack()

        frame3 = tk.Frame(self)
        frame3.pack(side="top", pady=(0, 15))

        self.warning_message = tk.Label(frame3, font=self.master.font, text='', fg='red')
        self.warning_message.pack()

        frame4 = tk.Frame(self)
        frame4.pack(side="top", pady=(0, 5))

        self.register_button = tk.Button(frame4, bg="white", width=30, font=self.master.btn_font, text="Log in",
                                         command=lambda: self.login(username_entry.get(), password_entry.get(),
                                                                    remember_me_var, self.warning_message, frame3))
        self.register_button.pack()

        self.button1 = tk.Button(self, bg="white", font=self.master.btn_font,
                                 text="Return to authorization page",
                                 command=lambda: self.master.switch_frame(AuthStartPage), width=30)
        self.button1.pack(side="top", pady=(0, 0))
