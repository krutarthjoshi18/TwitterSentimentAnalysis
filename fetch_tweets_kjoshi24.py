""" Author: Krutarth
    This piece of code solves the Part A of the homework
    It uses the Twitter API and generates the solutions
    as asked in the questions"""

import argparse
import oauth2 as oauth
import urllib.request as urllib
import json
import sys
import csv

# See Assignment 1 instructions for how to get these credentials
access_token_key = ""  # Enter keyshere
access_token_secret = ""

consumer_key = ""
consumer_secret = ""

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''


def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response


def fetch_samples():
    url = "https://stream.twitter.com/1.1/statuses/sample.json?language=en"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        print(line.decode("utf-8").strip())


def fetch_by_terms(term):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    parameters = [("q", term), ("count", 100)]
    response = twitterreq(url, "GET", parameters)
    print(response.readline().decode("utf-8"))


def fetch_by_user_names(user_name_file):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    temp_file = open(user_name_file)
    actors_temp = temp_file.read()
    temp_file.close()
    actors_list = actors_temp.split('\n')
    all_tweets = {}
    for actors in actors_list:
        actors = actors.strip()
        if actors:
            parameters = [("screen_name", actors), ("count", 100)]
            response = twitterreq(url, "GET", parameters)
            tweet = json.loads(response.read().decode("utf-8"))
            if response.status == 200:
                for current_tweet in tweet:
                    if actors in all_tweets.keys():
                        all_tweets[actors].append(current_tweet['text'])
                    else:
                        all_tweets[actors] = [current_tweet['text']]
    writer = csv.writer(sys.stdout)
    writer.writerow(["user_names", "tweets"])
    for single_user_name in all_tweets:
        for tweet in all_tweets[single_user_name]:
            writer.writerow([single_user_name, tweet])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', required=True, help='Enter the command')
    parser.add_argument('-term', help='Enter the search term')
    parser.add_argument('-file', help='Enter the user name file')
    opts = parser.parse_args()
    if opts.c == "fetch_samples":
        fetch_samples()
    elif opts.c == "fetch_by_terms":
        term = opts.term
        fetch_by_terms(term)
    elif opts.c == "fetch_by_user_names":
        user_name_file = opts.file
        fetch_by_user_names(user_name_file)
    else:
        raise Exception("Unrecognized command")
