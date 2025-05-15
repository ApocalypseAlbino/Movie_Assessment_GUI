from tkinter import *
import random
import csv
from functools import partial  # To prevent unwanted windows


def has_duplicates(data):
    return len(data) != len(set(data))


def get_questions():
    # Retrieve quotes from csv file and put them in a list
    file = open("movie_quotes.csv", "r")
    all_quotes = list(csv.reader(file, delimiter=","))
    file.close()

    # Remove the first row
    all_quotes.pop(0)

    round_quotes = []
    round_movies = []

    # loop until we have four quotes with different scores...
    while len(round_movies) < 4:
        potential_quote = random.choice(all_quotes)
        round_quotes.append(potential_quote[0])
        round_movies.append(potential_quote[1])
        if has_duplicates(round_movies):
            round_movies.pop()
            round_quotes.pop()
        else:
            continue

    question_list = ["What movie is the quote '' from?", "Which of these quotes are from the movie ''?"]

    question = random.choice(question_list)

    numbers = [0, 1, 2, 3]
    correct_num = random.choice(numbers)
    numbers.pop(correct_num)

    if question == "What movie is the quote '' from?":
        correct_quote = []
        correct_quote += round_quotes
        delete1 = numbers[0]
        delete2 = numbers[1]
        delete3 = numbers[2]
        del correct_quote[delete3]
        del correct_quote[delete2]
        del correct_quote[delete1]

        correct_ans = round_quotes[correct_num]
        round_qm = round_movies
        question_qm = correct_quote[0]
        question = f'What movie is the quote "{question_qm}" from?'

        return correct_ans, question_qm, question, round_qm

    else:
        correct_movie = []
        correct_movie += round_movies
        delete1 = numbers[0]
        delete2 = numbers[1]
        delete3 = numbers[2]
        del correct_movie[delete3]
        del correct_movie[delete2]
        del correct_movie[delete1]

        correct_ans = round_quotes[correct_num]
        round_qm = round_quotes
        question_qm = correct_movie[0]
        question = f"Which of these quotes are from the movie '{question_qm}'?"

        return correct_ans, question_qm, question, round_qm


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

        # rounds played - start with zero
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        # lists for question/answer details
        self.round_qm = []
        self.correct_ans = []

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.play_box = Toplevel()

        # If users press the 'x' on the game window, end the entire game!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Question",
                                   font=("Arial", "16", "bold"),
                                   wraplength=450)
        self.heading_label.grid(row=0, pady=10)

        # Colour buttons
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        # colour buttons (text | bg colour | command | row | column)
        answer_details_list = [
            ["Answer", "#3B90BA", "", 0, 0],
            ["Answer", "#3B90BA", "", 0, 1],
            ["Answer", "#3B90BA", "", 1, 0],
            ["Answer", "#3B90BA", "", 1, 1]
        ]

        # List to hold buttons once they have been made
        self.answer_ref_list = []

        for item in answer_details_list:
            self.make_button = Button(self.colour_frame,
                                      text=item[0], bg=item[1],
                                      fg="#000", font=("Arial", "12", "bold"),
                                      width=22, wraplength="200", command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)

            self.answer_ref_list.append(self.make_button)

        self.result_label = Label(self.game_frame, text="Correct/Incorrect! Good/Bad job!",
                                  font=("Arial", "12"), bg="#b4daa9")
        self.result_label.grid(row=4, pady=10)

        # Other buttons
        self.button_frame = Frame(self.game_frame)
        self.button_frame.grid(row=6)

        # buttons (text | bg colour | command | row | column | fg colour)
        button_details_list = [
            [f"Next Round (1/{how_many})", "#34A300", self.new_round, 0, 1, "#000"],
            ["Instructions", "#E0DD00", "", 0, 0, "#000"]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg=item[5], font=("Arial", "16", "bold"),
                                      width=15, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=6)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", "16", "bold"),
                                      fg="#fff", bg="#CC0700",
                                      command=self.close_play,
                                      width=32)
        self.end_game_button.grid(row=7, pady=10)

        # Once interface has been created, invoke new round function for first round
        self.new_round()

    def new_round(self):
        """
        Chooses four colours, works out median for score to beat. Configures buttons
        with chosen colours
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get questions (both types) and answers...
        self.correct_ans, question_qm, question, round_qm = get_questions()

        # Hide results label and put the question in the label
        self.heading_label.config(text=question)
        self.result_label.config(text=f"{'=' * 7}", bg="#f0f0f0")

        for count, item in enumerate(self.answer_ref_list):
            item.config(text=round_qm[count], state=NORMAL)

        # self.next_round_button.config(state=DISABLED)

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
