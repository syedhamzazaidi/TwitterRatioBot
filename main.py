import requests
import os

try:
    BEARER_TOKEN = os.environ['BEARER_TOKEN']
except:
    print("BEARER_TOKEN missing from environment. Export and try again")
    exit(1)


def get_tweetfields(id, tweetfields="public_metrics"):
    url = "https://api.twitter.com/2/tweets?ids={}&tweet.fields={}".format(id, tweetfields)
    resp = requests.get(url, headers={"Authorization": "Bearer {}".format(BEARER_TOKEN)})
    return resp.json()

def get_likes(id):
    return get_tweetfields(id, "public_metrics")["data"][0]["public_metrics"]["like_count"]

def get_parent_tweet(id):
    return get_tweetfields(id, "referenced_tweets")["data"][0]["referenced_tweets"][0]["id"]


if __name__ == "__main__":
    id = '1480713640772730880'
    id = id if id else input()

    son_like = get_likes(id)
    parent_like = get_likes(get_parent_tweet(id))
    print("ratio = ", son_like/parent_like, "boom son")