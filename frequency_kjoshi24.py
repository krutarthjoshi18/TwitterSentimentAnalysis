""" Author: Krutarth
    This piece of code solves the Part A of the homework
    It uses the Twitter API and generates the solutions
    as asked in the questions"""

import json
import sys


def main():
    tweet_file = open(sys.argv[2])
    frequency_tuple = getTerms(tweet_file)
    word_frequency_list = compute_term_frequency(frequency_tuple)

    # -------------------------
    # To generate term_freq.txt
    # -------------------------
    # for i in range(0, len(word_frequency_list)):
    #     print(word_frequency_list[i][0] + " " + str(word_frequency_list[i][1]))

    # -------------------------
    # To generate reporta.txt
    # -------------------------
    top30_words = word_frequency_list[0:30]
    for i in range(0, len(top30_words)):
        print(top30_words[i][0] + " " + str(top30_words[i][1]))
    tweet_file.close()


def generateStopwordsList():
    stopwords_file = open(sys.argv[1])
    stopwords_list = []
    for line in stopwords_file:
        line = line.replace('\n', "")
        stopwords_list.append(line)
    return stopwords_list


def getTerms(file_stream):
    stopwords = generateStopwordsList()
    unique_word = set()
    word_frequency_dictionary = {}
    total_wordcount = 0
    for line in file_stream:
        current_tweet_raw = json.loads(line)
        current_tweet_clean = current_tweet_raw['text'].split(" ")
        for word in current_tweet_clean:
            if word.isalpha():
                total_wordcount += 1
                if str.lower(word) not in stopwords:
                    if word not in unique_word:
                        word_frequency_dictionary[word] = 1
                        unique_word.add(word)
                    else:
                        word_frequency_dictionary[word] += 1
    return word_frequency_dictionary, total_wordcount


def compute_term_frequency(input_tuple):
    total_words = input_tuple[1]
    frequency_dict = input_tuple[0]
    term_frequency_list = []
    for word in frequency_dict.keys():
        term_frequency_list.append((word, frequency_dict[word] / total_words))
    term_frequency_list.sort(key=lambda x: x[1], reverse=True)
    return term_frequency_list


if __name__ == '__main__':
    main()
