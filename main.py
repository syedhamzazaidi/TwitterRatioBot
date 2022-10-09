import os
import requests

try:
    BEARER_TOKEN = os.environ['BEARER_TOKEN']
except:
    print("BEARER_TOKEN missing from credentials. Add credentials and try again")
    exit(1)

header = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}

def load_already_replied():
    try:
        with open("already_replied.txt", "r") as file:
            already_replied = set(file.read().splitlines())
    except:
        already_replied = set()
    return already_replied

def get_mentions():
    url = "https://api.twitter.com/2/users/1578989916377096193/mentions"
    resp = requests.get(url, headers=header)
    return reversed([data['id'] for data in resp.json()['data']])

def reply(id):
    parent_id = get_parent_tweet(id)
    parent_like_count = get_likes(parent_id)
    grandparent_id = get_parent_tweet(parent_id)
    grandparent_like_count = get_likes(grandparent_id)

    ratio = grandparent_like_count / parent_like_count

    if ratio > 1:
        reply_string = f"Damn son that's a ratio of {ratio} ! 🔥"
    else:
        reply_string = f"Eh, ratio's just {ratio}. Do better next time."

    print(reply_string)

def get_tweetfields(id, tweetfields="public_metrics"):
    url = "https://api.twitter.com/2/tweets?ids={}&tweet.fields={}".format(id, tweetfields)
    resp = requests.get(url, headers=header)
    return resp.json()

def get_likes(id):
    return get_tweetfields(id, "public_metrics")["data"][0]["public_metrics"]["like_count"]

def get_parent_tweet(id):
    return get_tweetfields(id, "referenced_tweets")["data"][0]["referenced_tweets"][0]["id"]


if __name__ == "__main__":
    mentions = get_mentions()
    already_replied = load_already_replied()
    with open('already_replied.txt', 'a') as file:
        for id in mentions:
            if id in already_replied:
                continue
            try:
                reply(id)
            except Exception as E:
                print("Could not reply: ", E)
            finally:
                file.write(id + '\n')
