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

        correct_ans = round_movies[correct_num]
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

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 12, "bold"),
                                      width=20)
        self.num_rounds_entry.grid(row=0, padx=10, pady=10)

        # Create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
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

        # Reset label and entry box
        self.choose_label.config(fg="#000", font=("Arial", 12, "bold"),
                                 text="How many questions do you want?")
        self.num_rounds_entry.config(bg="#fff")
        self.num_rounds_entry.delete(0, END)

        error = "Choose a whole number between 1 and 100"
        has_errors = "no"

        # checks that amount to be converted is a number above 0 and less than 101
        try:
            rounds_wanted = int(rounds_wanted)
            if 1 <= rounds_wanted & rounds_wanted <= 100:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ieL hide rounds choice window)
                root.withdraw()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the errors if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000")
            self.num_rounds_entry.config(bg="#f4cccc")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for the quiz
    """

    def __init__(self, how_many):

        # lists for question/answer details
        self.round_qm = []
        self.correct_ans = []

        # How many rounds wanted and played
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()

        self.play_box = Toplevel()

        # If users press the 'x' on the game window, end the entire game!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # Frame so question and winrate are side by side
        self.heading_frame = Frame(self.game_frame)
        self.heading_frame.grid(row=0)

        self.heading_label = Label(self.heading_frame, text="Question",
                                   font=("Arial", 16, "bold"),
                                   wraplength=375)
        self.heading_label.grid(row=0, column=0, pady=10)

        self.winrate_label = Label(self.heading_frame, text=f"Score: 0/{how_many}",
                                   font=("Arial", 12, "bold"))
        self.winrate_label.grid(row=0, column=2, padx=15)

        # Frame for answer buttons
        self.answer_frame = Frame(self.game_frame)
        self.answer_frame.grid(row=3)

        # details for the answer buttons (text | row | column | ID)
        answer_details_list = [
            ["Answer", 0, 0, 0],
            ["Answer", 0, 1, 1],
            ["Answer", 1, 0, 2],
            ["Answer", 1, 1, 3]
        ]

        # List to hold buttons once they have been made
        self.answer_ref_list = []

        for item in answer_details_list:
            self.make_button = Button(self.answer_frame,
                                      text=item[1], bg="#4D9EC7",
                                      fg="#000", font=("Arial", 12, "bold"),
                                      width=22, height=4, wraplength="200",
                                      command=partial(self.round_results, item[3]))
            self.make_button.grid(row=item[1], column=item[2], padx=5, pady=5)

            self.answer_ref_list.append(self.make_button)

        self.result_label = Label(self.game_frame, text="Correct/Incorrect! Good/Bad job!",
                                  font=("Arial", 12), bg="#b4daa9")
        self.result_label.grid(row=4, pady=10)

        # Frame for next round and instruction buttons
        self.button_frame = Frame(self.game_frame)
        self.button_frame.grid(row=6)

        # buttons (text | bg colour | command | row | column | fg colour)
        button_details_list = [
            [f"Next Round (0/0)", "#34A300", self.new_round, 0, 1, "#000"],
            ["Instructions", "#E18B35", self.to_instr, 0, 0, "#000"]
        ]

        # List to hold buttons once they have been made
        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg=item[5], font=("Arial", 16, "bold"),
                                      width=15, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=6)

            self.button_ref_list.append(self.make_button)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", 16, "bold"),
                                      fg="#fff", bg="#CC0700",
                                      command=self.close_play,
                                      width=32)
        self.end_game_button.grid(row=7, pady=10)

        self.next_round_button = self.button_ref_list[0]
        self.instructions_button = self.button_ref_list[1]

        # Once interface has been created, invoke new round function for first round
        self.new_round()

    def new_round(self):
        """
        Chooses question and answers, and puts them in the buttons/label
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

        # Configure next round button to say how many rounds has been, and say "last round" accordingly
        if rounds_played == rounds_wanted:
            self.next_round_button.config(text=f"Last round")
            self.next_round_button.config(state=DISABLED)
        else:
            self.next_round_button.config(text=f"Next round ({rounds_played}/{rounds_wanted})")

        for count, item in enumerate(self.answer_ref_list):
            item.config(text=round_qm[count], state=NORMAL, bg="#4D9EC7")

        self.next_round_button.config(state=DISABLED)

    def round_results(self, user_choice):
        """
        Retrieves which button was pushed, checks whether
        it is correct or not, and displays such
        """

        # Retrieve text from button pressed
        which_ans = self.answer_ref_list[user_choice].cget('text')

        # Retrieve rounds wanted/played
        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        # Re-enable next round button if not last round
        if rounds_played != rounds_wanted:
            self.next_round_button.config(state=NORMAL)

        # Edit tag to say whether user was right or wrong and add score to winrate if correct
        if which_ans == self.correct_ans:
            result_text = f"Congrats! That was the correct answer!"
            result_bg = "#82b366"

            rounds_won = self.rounds_won.get()
            rounds_won += 1
            self.rounds_won.set(rounds_won)
            self.winrate_label.config(text=f"Score: {rounds_won}/{rounds_wanted}")

        else:
            result_text = f"Eesh. That was incorrect, sorry"
            result_bg = "#f8cecc"

        self.result_label.config(text=result_text, bg=result_bg)


        # Disable answer buttons and colour correct answers green and wrong answers red
        for count, item in enumerate(self.answer_ref_list):
            item.config(state=DISABLED)
            text = item.cget("text")
            if text == self.correct_ans:
                item.config(bg="#1eb333", disabledforeground="#000")
            elif text == which_ans and text != self.correct_ans:
                item.config(bg="#e42723", disabledforeground="#000")
            else:
                item.config(bg="#b2aead", disabledforeground="#000")

    def close_play(self):
        # Reshow root and end current quiz
        root.deiconify()
        self.play_box.destroy()

    def to_instr(self):
        """
        Displays instructions for quiz
        """
        Instructions(self)

class Instructions:

    def __init__(self, partner):

        # set up dialogue box and background color
        background = "#ffe6cc"
        self.instructions_box = Toplevel()

        # disable buttons
        partner.instructions_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)

        # If users press 'X' instead of dismiss, do the same thing
        self.instructions_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_instructions, partner))

        self.instructions_frame = Frame(self.instructions_box, width=300,
                                height=200)
        self.instructions_frame.grid()

        self.instructions_heading_label = Label(self.instructions_frame,
                                        text="Instructions",
                                        font=("Arial", 14, "bold"))
        self.instructions_heading_label.grid(row=0)

        instructions_text = "How to play:\n" \
                    "Choose the number of questions\n"\
                    "Enter how many quiz questions you want to answer (1–100) and click Play.\n\n" \
                    "You will be asked either:\n" \
                    "Which movie a quote is from, or\n" \
                    "Which quote is from a specific movie\n\n" \
                    "Choose the correct answer from the four options.\n" \
                    "You'll see if your answer was correct.\n\n" \
                    "Click 'Next Round'\n" \
                    "Move on to the next question. The button will show how many questions you've done.\n\n" \
                    "Click 'End Game'\n" \
                    "You can end the quiz at any time by clicking the End Game button."

        self.instructions_text_label = Label(self.instructions_frame,
                                     text=instructions_text, wraplength=350,
                                     justify="left")
        self.instructions_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.instructions_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#E18B35",
                                     fg="#000",
                                     command=partial(self.close_instructions, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List of everything to put background colour on
        recolour_list = (self.instructions_frame, self.instructions_heading_label,
                         self.instructions_text_label)

        for item in recolour_list:
            item.config(bg=background)

    def close_instructions(self, partner):
        # Re-enable the buttons
        partner.instructions_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)

        self.instructions_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quote Quiz")
    StartQuiz()
    root.mainloop()
