import csv
import random


# def round_ans(val):
#     """
#     Rounds numbers to nearest integer
#     :param val: number to be rounded
#     :return: rounded number
#     """
#     var_rounded = (val * 2 + 1) // 2
#     raw_rounded = "{:.0f}".format(var_rounded)
#     return int(raw_rounded)


# Retrieve quotes from csv file and put them in a list
file = open("movie_quotes.csv", "r")
all_quotes = list(csv.reader(file, delimiter=","))
file.close()

# Remove the first row
all_quotes.pop(0)

round_quotes = []
round_movies = []

# loop until we have four quotes with different scores...
while len(round_quotes) < 4:
    potential_quote = random.choice(all_quotes)
    round_quotes.append(potential_quote[0])
    round_movies.append(potential_quote[1])

print(round_quotes)
print(round_movies)
