import customtkinter as ctk


# TODO: make the button auto scale (essentially for custom)

def countX(lst, x):
    """counts the number of occurrences of x in lst"""
    count = 0
    for ele in lst:
        for ele2 in ele:
            try:
                if type(ele2[0]) == x:
                    count = count + 1
            except TypeError:
                continue

    return count


# noinspection PyTypeChecker,PyUnresolvedReferences
class Interface(ctk.CTk):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.flags_number = 0
        self.game_grid = self.app.algo.grid
        self.size = self.app.size
        self.position_checked = []

        # initializing variables
        self.top_frame = None
        self.main_frame = None
        self.inner_frame = None
        self.title_label = None
        self.flags_label = None
        self.name_label = None
        self.buttons = []
        self.flagged_list = []
        self.is_color_changing_finished = False

        # configure window
        self.title("MineSweeper")
        self.geometry(f"{1100}x{580}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.grid_rowconfigure(1, weight=1)

        self.generate_top_frame()
        self.generate_main_frame()

    def generate_top_frame(self):
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        for i in range(3):
            self.top_frame.grid_columnconfigure(i, weight=1)

        self.title_label = ctk.CTkLabel(self.top_frame, text="MineSweeper", font=("Courier", 30))
        self.title_label.grid(row=0, column=1, pady=10, sticky="ew")

        self.flags_label = ctk.CTkLabel(
            self.top_frame,
            text=f"{self.flags_number}/{self.app.mine_number}",
            font=("Courier", 20)
        )
        self.flags_label.grid(row=0, column=0, sticky="ew")

        self.name_label = ctk.CTkLabel(self.top_frame, text='Fauchet Malo', font=("Courier", 20))
        self.name_label.grid(row=0, column=2, pady=10, sticky="ew")

    def generate_main_frame(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, padx=10, pady=10, sticky="news")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.inner_frame = ctk.CTkFrame(self.main_frame)
        self.inner_frame.grid(row=0, column=0)

        grid_size = self.app.size
        for y in range(grid_size[1]):
            self.inner_frame.grid_rowconfigure(y, weight=0)
        for x in range(grid_size[0]):
            self.inner_frame.grid_columnconfigure(x, weight=0)

        event = 0  # It gets replaced by the event of the button clicked when right-clicked on the button
        # cause custom tkinter absolutely wanted to send it in the lambda used below in the .bind
        # It is the only way around that bug

        # generate buttons
        self.buttons = []
        for y in range(grid_size[1]):
            self.buttons.append([])
            for x in range(grid_size[0]):
                button_position = (x, y)
                self.buttons[y].append([ctk.CTkButton(
                    self.inner_frame,
                    text='',
                    width=25,
                    command=lambda buttons_position=button_position: self.button_clicked(buttons_position)
                ), False])
                self.buttons[y][x][0].grid(row=y, column=x, pady=0, padx=0, sticky="news")
                self.buttons[y][x][0].bind(
                    '<Button-3>',
                    lambda ctk_event=event, x_coord=x, y_coord=y: self.change_color(ctk_event, x_coord, y_coord)
                )  # binding the right click to the flagging method

    def update_button(self, position):
        """update the button at position"""
        x, y = position
        case_value = self.game_grid[y][x]

        flagged = self.buttons[y][x][1]
        if flagged:
            self.flags_number -= 1
            self.flags_label.configure(text=f"{self.flags_number}/{self.app.mine_number}")

        self.buttons[y][x][0].destroy()
        self.buttons[y].pop(x)

        self.buttons[y].insert(x, ctk.CTkLabel(self.inner_frame, text=f"{case_value}", width=25))
        self.buttons[y][x].grid(row=y, column=x, pady=0, padx=0, sticky="news")

        if (self.flags_number <= self.app.mine_number) and countX(self.buttons, ctk.CTkButton) == self.app.mine_number:
            self.handle_end_game(1)

    def discover_case_around(self, position):
        """Discovers the case around the position one if the position one is a zero"""
        if position in self.position_checked:  # dodges rediscovering 0's already discovered
            return

        self.position_checked.append(position)
        x, y = position
        case_value = self.game_grid[y][x]

        if case_value == 0:
            # check up
            if y != 0:
                self.discover_case_around((x, y - 1))
                # check up left
                if x != 0:
                    self.discover_case_around((x - 1, y - 1))
                # check up right
                if x != self.size[0] - 1:
                    self.discover_case_around((x + 1, y - 1))

            # check left
            if x != 0:
                self.discover_case_around((x - 1, y))
            # check right
            if x != self.size[0] - 1:
                self.discover_case_around((x + 1, y))

            # check down
            if y != self.size[1] - 1:
                self.discover_case_around((x, y + 1))
                # check down left
                if x != 0:
                    self.discover_case_around((x - 1, y + 1))
                # check down right
                if x != self.size[0] - 1:
                    self.discover_case_around((x + 1, y + 1))

        self.update_button(position)

    def button_clicked(self, position):
        """
        The button_clicked function is called when a button is clicked.
        It clicked on a 0
        Then, depending on what value the case has (0-8 or -2), it will either discover all adjacent cases or end the game in defeat.
        If there are no more flags left and all mines have been flagged, then you win.

        :param self: Refer to the instance of the class
        :param position: Know which button was clicked
        :return: Nothing
        """

        x, y = position
        case_value = self.game_grid[y][x]

        if case_value == 0:
            self.discover_case_around(position)
            return
        elif case_value == -1:
            self.handle_end_game(0)
            return

        self.position_checked.append(position)
        self.update_button(position)

    def change_color(self, event, x, y):
        del event
        flagged = self.buttons[y][x][1]

        if not flagged:
            self.flags_number += 1
            self.flags_label.configure(text=f"{self.flags_number}/{self.app.mine_number}")
            self.buttons[y][x][0].configure(fg_color='red')
            self.buttons[y][x][1] = True
            self.flagged_list.append((x, y))
            if (self.app.mine_number == self.flags_number) and countX(self.buttons, ctk.CTkButton) == self.app.mine_number:
                self.end_game_win()
        else:
            self.flags_number -= 1
            self.flags_label.configure(text=f"{self.flags_number}/{self.app.mine_number}")
            self.buttons[y][x][0].configure(fg_color="#1f6aa5")
            self.buttons[y][x][1] = False
            self.flagged_list.remove((x, y))

    def end_game_color_button(self, pointer=0):
        """
        RECURSIVE
        Changes the color of the mines: green if you flagged it, red if you didn't and purple for the one you
        flagged but wasn't actually a mine
        """
        # TODO: make the color purple if the user flagged a non-mine → fix cause it works sometimes
        positions = self.app.algo.mine_position

        # add any flag that isn't on a mine
        if not pointer:
            for flag in self.flagged_list:
                if flag not in positions:
                    positions.append(flag)

        if pointer == len(positions):
            return

        y, x = positions[pointer]
        if self.buttons[y][x][1]:  # if the case is flagged
            if self.game_grid[y][x] != -1:
                self.buttons[y][x][0].configure(fg_color='purple')
            else:
                self.buttons[y][x][0].configure(fg_color='green')
        else:
            self.buttons[y][x][0].configure(fg_color='red')
        self.update()
        return self.after(50, lambda list_pointer=pointer: self.end_game_color_button(list_pointer + 1))

    def retry_window(self, win_lost_text):
        """Lets you choose if you want to retry (with which difficulty) or if you want to quit"""
        retry = ctk.CTkToplevel(self)
        retry.title(win_lost_text)
        retry.geometry(f"{400}x{375}")
        retry.grab_set()

        win_lost_text_label = ctk.CTkLabel(retry, text=f"{win_lost_text}Want to try again ?", font=("Courier", 24))
        win_lost_text_label.pack(pady=10)

        button_easy = ctk.CTkButton(retry, text="Easy", command=lambda: self.app.retry(0))
        button_easy.pack(pady=10)

        button_intermediate = ctk.CTkButton(retry, text="Intermediate", command=lambda: self.app.retry(1))
        button_intermediate.pack(pady=10)

        button_hard = ctk.CTkButton(retry, text="Hard", command=lambda: self.app.retry(2))
        button_hard.pack(pady=10)

        button_custom = ctk.CTkButton(retry, text="Custom", command=lambda: self.app.retry(3))
        button_custom.pack(pady=10)

        button_quit = ctk.CTkButton(retry, text="QUIT", width=35, command=self.quit)
        button_quit.pack(pady=(30, 0))

    def deactivate_buttons(self):
        for button_list in self.buttons:
            for button in button_list:
                try:
                    button[0].configure(state="disabled")
                except TypeError:
                    pass

    def handle_end_game(self, state):
        """
        calls the different method concerning the end of the game considering if the user won or lost
        :param: state: 0 = lost, 1 = won
        """
        self.deactivate_buttons()
        time_taken = self.app.algo.mine_number * 55  # time it'll take for the color change to finish

        if state:
            self.after(time_taken, lambda: self.retry_window("You win! What a miracle!\n"))
        else:
            self.after(time_taken, lambda: self.retry_window("You lost. What a shame.\n"))

        self.end_game_color_button()
