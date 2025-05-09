from tkinter import *
from functools import partial  # To prevent unwanted windows


class StartQuiz:
    """
    Initial interface which asks users how many rounds they want
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for labels
        intro_string = "This is a multi-choice quiz about quotes from movies. You will either select which movie a " \
                       "quote comes from, or select which quote belongs to a certain movie."

        choose_string = "How many questions do you want?"

        # List of labels to be made (text | font)
        start_labels_list = [
            ["Welcome to the Movie Quotes Quiz", ("Arial", "15", "bold")],
            [intro_string, ("Arial", "12")],
            [choose_string, ("Arial", "12", "bold")]
        ]

        # Create labels and add them to the reference list

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0],
                               font=item[1], wraplength=350,
                               justify="left", padx=20, pady=10)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # Extract choice label so that it can be changed to an error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=20)
        self.num_rounds_entry.grid(row=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#000", bg="#8FA8F3", text="Play", width=12,
                                  command=self.check_rounds)
        self.play_button.grid(row=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve amount of rounds wanted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box
        self.choose_label.config(fg="#000", font=("Arial", "12", "bold"),
                                 text="How many questions do you want?")
        self.num_rounds_entry.config(bg="#fff")
        self.num_rounds_entry.delete(0, END)

        error = "Please choose a whole number more than 0"
        has_errors = "no"

        # checks that amount to be converted is a number above 0
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ieL hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000")
            self.num_rounds_entry.config(bg="#f4cccc")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for the quiz
    """

    def __init__(self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text="Question",
                                        font=("Arial", "16", "bold"))
        self.game_heading_label.grid(row=0, pady=10)

        # Colour buttons
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        # colour buttons (text | bg colour | command | row | column)
        answer_details_list = [
            ["Answer", "#f0f0f0", "", 0, 0],
            ["Answer", "#f0f0f0", "", 0, 1],
            ["Answer", "#f0f0f0", "", 1, 0],
            ["Answer", "#f0f0f0", "", 1, 1]
        ]

        # List to hold buttons once they have been made
        self.answer_ref_list = []

        for item in answer_details_list:
            self.make_button = Button(self.colour_frame,
                                      text=item[0], bg=item[1],
                                      fg="#000", font=("Arial", "12"),
                                      width=22, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)

            self.answer_ref_list.append(self.make_button)

        self.result_label = Label(self.game_frame, text="Correct/Incorrect! Good/Bad job!",
                                  font=("Arial", "12"), bg="#b4daa9")
        self.result_label.grid(row=4, pady=10)

        # Other buttons
        self.button_frame = Frame(self.game_frame)
        self.button_frame.grid(row=6)

        # buttons (text | bg colour | command | row | column)
        button_details_list = [
            [f"Next Round (1/{how_many})", "#f0f0f0", "", 0, 1],
            ["Instructions", "#f0f0f0", "", 0, 0]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#000", font=("Arial", "16", "bold"),
                                      width=15, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=6)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", "16", "bold"),
                                      fg="#000", bg="#f0f0f0",
                                      command=self.close_play,
                                      width=32)
        self.end_game_button.grid(row=7, pady=10)

    def close_play(self):
        # Reshow root and end current quiz
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quote Quiz")
    StartQuiz()
    root.mainloop()
