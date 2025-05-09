import csv
import random


def has_duplicates(data):
    return len(data) != len(set(data))


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

print(round_quotes)
print(round_movies, "\n")

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
    question_quote = correct_quote[0]
    question = f'What movie is the quote "{question_quote}" from?'

    print(question)
    print(correct_ans)
    print(round_movies)

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
    question_movie = correct_movie[0]
    question = f"Which of these quotes are from the movie '{question_movie}'?"

    print(question)
    print(correct_ans)
    print(round_quotes)
