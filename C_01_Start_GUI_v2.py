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

        # choose_string = "Oops - Please choose a whole number more than 0."
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

        # Bind enter to play button
        root.bind('<Return>', lambda event: self.check_rounds())

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve amount of rounds wanted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#ffffff")

        error = "Please choose a whole number more than 0"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute 0
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # temporary success message, replace with call to PlayGame class
                self.choose_label.config(text=f"You have chosen to play {rounds_wanted} "
                                              f"round/s")
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000")
            self.num_rounds_entry.config(bg="#f4cccc")
            self.num_rounds_entry.delete(0, END)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quote Quiz")
    StartQuiz()
    root.mainloop()
