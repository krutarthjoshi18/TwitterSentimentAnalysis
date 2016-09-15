""" Author: Krutarth
    This piece of code solves the Part B of the homework
    It uses the Twitter API and generates the solutions
    as asked in the questions"""

import json
import sys


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sent_score_dict = generate_sentiment_dictionary(sent_file)
    sent_file.close()
    tweet_sentiment = generate_sentiment_score(sent_score_dict, tweet_file)
    top10_tweets = tweet_sentiment[0:10]
    bottom10_tweets = tweet_sentiment[-11:-1]
    for i in range(0, 10):
        print(str(top10_tweets[i][0]) + ": " + top10_tweets[i][1].replace("\n", " "))
    for i in range(0, 10):
        print(str(bottom10_tweets[i][0]) + ": " + bottom10_tweets[i][1].replace("\n", " "))
    tweet_file.close()


def generate_sentiment_dictionary(sentiment_file):
    sentiment_score = {}
    for line in sentiment_file:
        sent_score = line.split("\t")
        sentiment_score[sent_score[0]] = float(sent_score[1])
    return sentiment_score


def generate_sentiment_score(sentiment_score, tweet_file):
    tweet_sentiment = []
    for line in tweet_file:
        current_tweet_raw = json.loads(line)
        current_tweet_clean = current_tweet_raw['text']
        current_tweet_splitted = current_tweet_clean.split(" ")
        current_tweet_score = 0.0
        for word in current_tweet_splitted:
            if word.isalpha():
                word = word.lower()
                if word in sentiment_score.keys():
                    current_tweet_score += sentiment_score[word]
        tweet_sentiment.append((current_tweet_score, current_tweet_clean))
    tweet_sentiment.sort(key=lambda x: x[0], reverse=True)
    return tweet_sentiment


if __name__ == '__main__':
    main()
