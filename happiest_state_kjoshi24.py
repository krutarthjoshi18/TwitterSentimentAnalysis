""" Author: Krutarth
    This piece of code solves the Part B of the homework
    It uses the Twitter API and generates the solutions
    as asked in the questions"""

import json
import sys


def main():
    sent_file = open(sys.argv[1])
    sent_score_dict = generate_sentiment_dictionary(sent_file)
    sent_file.close()
    state_file = open("state_abbreviations.txt", "r")
    state_dict = generate_state_abbreviation_dictionary(state_file)
    state_file.close()
    tweet_file = open(sys.argv[2])
    resu = get_happiest_state(sent_score_dict, tweet_file, state_dict)
    happiest_state = resu[0:5]
    saddest_state = resu[-6:-1]
    for line in happiest_state:
        print(str(line[0]) + ": " + line[1])
    for line in saddest_state:
        print(str(line[0]) + ": " + line[1])
    tweet_file.close()


def generate_state_abbreviation_dictionary(file):
    state_abbre = {}
    for line in file:
        tuple = line.split(",")
        state_abbre[tuple[0]] = tuple[1][:-1]
    return state_abbre


def generate_sentiment_dictionary(sentiment_file):
    sentiment_score = {}
    for line in sentiment_file:
        word, score = line.split("\t")
        sentiment_score[word] = float(score)
    return sentiment_score


def get_happiest_state(sent_score, tweet_file, state_dict):
    state_wise_tweet = {}
    for line in tweet_file:
        current_tweet_raw = json.loads(line)
        current_tweet_clean = current_tweet_raw['text']
        current_tweet_location = current_tweet_raw['place']
        if current_tweet_location is not None:
            current_tweet_country = current_tweet_location['country_code']
            if current_tweet_country.strip() == "US":
                narrowed_location = current_tweet_location['full_name'].split(',')
                if len(narrowed_location) == 2:
                    if narrowed_location[-1].strip() == "USA":
                        add_statewise_tweet(state_wise_tweet, narrowed_location[0].strip(), current_tweet_clean)
                    else:
                        add_statewise_tweet(state_wise_tweet, state_dict[narrowed_location[-1].strip()],
                                            current_tweet_clean)
    return get_happiness_factor(sent_score, state_wise_tweet, state_dict)


def get_happiness_factor(dic_sent, dic_state, state_dict):
    happy_state = []
    for state in dic_state.keys():
        current_state_score = 0.0
        num_tweets = len(dic_state[state])
        for tweet in dic_state[state]:
            word_list = tweet.split(" ")
            for word in word_list:
                if word.isalpha():
                    word = word.lower()
                    if word in dic_sent.keys():
                        current_state_score += dic_sent[word]
        happy_state.append(
            (current_state_score / num_tweets, list(state_dict.keys())[list(state_dict.values()).index(state)]))
    happy_state.sort(key=lambda x: x[0], reverse=True)
    return happy_state


def add_statewise_tweet(dict, key, value):
    if key not in dict.keys():
        dict[key] = [value]
    else:
        dict[key].append(value)
    return dict


if __name__ == '__main__':
    main()
