import os
import requests

class Twitter():

    def __init__(self):
        self.url = "https://api.twitter.com/2/"
        try:
            self.BEARER_TOKEN = os.environ['BEARER_TOKEN']
            self.CLIENT_ID = os.environ['CLIENT_ID']
            self.refreshed_token = os.environ['TOKEN']
        except:
            print("Initial credentials missing. Add credentials to environment and try again")
            exit(1)
        self.header = {"Authorization": "Bearer {}".format(self.BEARER_TOKEN)}
        self.refresh_token()

    def refresh_token(self):
        uri = "oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            "refresh_token": f"{self.refreshed_token}",
            "grant_type": "refresh_token",
            "client_id": f"{self.CLIENT_ID}"
        }
        resp = requests.post(self.url+uri, headers=headers, data=payload).json()
        print("refresh\n", resp)
        self.access_token = resp['access_token']
        self.refreshed_token = os.environ['TOKEN'] = resp['refresh_token']
        return resp

    def get_mentions(self):
        uri = "users/1578989916377096193/mentions"
        resp = requests.get(self.url+uri, headers=self.header)
        return reversed([data['id'] for data in resp.json()['data']])

    def get_likes(self, id):
        return self.get_tweetfields(id, "public_metrics")["data"][0]["public_metrics"]["like_count"]

    def get_parent_tweet(self, id):
        return self.get_tweetfields(id, "referenced_tweets")["data"][0]["referenced_tweets"][0]["id"]

    def post_reply_tweet(self, text, parent_id):
        uri = "tweets"
        header = {
            "Content-type": "application/json",
            "Authorization": f"OAuth {self.access_token}"
            }
        payload = {
            "text": f"{text}",
            "in_reply_to_tweet_id": parent_id,
        }
        resp = requests.post(self.url+uri, headers=header, params=payload)
        print(resp.text)
        return resp.json()

    def get_tweetfields(self, id, tweetfields="public_metrics"):
        uri = "tweets?ids={}&tweet.fields={}".format(id, tweetfields)
        resp = requests.get(self.url+uri, headeurlrs=self.header)
        return resp.json()

if __name__ == '__main__':
    tweepy = Twitter()