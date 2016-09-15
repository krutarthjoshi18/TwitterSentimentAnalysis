""" Author: Krutarth
    This piece of code solves the Part B of the homework
    It uses the Twitter API and generates the solutions
    as asked in the questions"""

import sys
import csv


def main():
    sent_file = open(sys.argv[1])
    sentiment_score_dict = generate_sentiment_dictionary(sent_file)
    sent_file.close()
    csv_file = open(sys.argv[2])
    csv_file.readline()
    file_reader = csv.reader(csv_file)
    tweet_dictionary = generate_actor_tweet_dictionary(file_reader)
    csv_file.close()
    happiness_score = get_happiest_actor(sentiment_score_dict, tweet_dictionary)
    for actors in happiness_score:
        print(str(actors[1]) + ": " + actors[0])


def generate_actor_tweet_dictionary(csv_file):
    tweet_dictionary = {}
    for line in csv_file:
        if line[0] in tweet_dictionary.keys():
            tweet_dictionary[line[0]].append(line[1])
        else:
            tweet_dictionary[line[0]] = [line[1]]
    return tweet_dictionary


def get_happiest_actor(sent_dict, tweet_dict):
    actor_happiness = []
    for actor in tweet_dict.keys():
        current_actor_score = 0.0
        current_tweet_list = tweet_dict[actor]
        tweet_count = len(current_tweet_list)
        for tweets in current_tweet_list:
            word_list = tweets.split(" ")
            for word in word_list:
                if word.isalpha():
                    word = word.lower()
                    if word in sent_dict.keys():
                        current_actor_score += sent_dict[word]
        actor_happiness.append((actor, float(current_actor_score / tweet_count)))
    actor_happiness.sort(key=lambda x: x[1], reverse=True)
    return actor_happiness


def generate_sentiment_dictionary(sentiment_file):
    sentiment_score = {}
    for line in sentiment_file:
        word, score = line.split("\t")
        sentiment_score[word] = float(score)
    return sentiment_score


if __name__ == '__main__':
    main()
