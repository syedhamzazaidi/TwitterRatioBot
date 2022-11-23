import os
import requests
from datetime import datetime, timedelta

class Twitter():

    def __init__(self, code=None):
        self.url = "https://api.twitter.com/2/"
        try:
            if code:
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                data = {
                    "code": code,
                    "grant_type": "authorization_code",
                    "client_id": os.environ['CLIENT_ID'],
                    "redirect_uri": os.environ['REDIRECT_URI'],
                    "code_verifier": "challenge"
                }
                response = requests.post(self.url + 'oauth2/token', headers=headers, data=data)
                os.environ['TOKEN'] = response.json()['refresh_token']
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
        self.access_token = resp['access_token']
        self.refreshed_token = os.environ['TOKEN'] = resp['refresh_token']
        return resp

    def get_mentions(self):
        uri = "users/1578989916377096193/mentions"
        yesterday = datetime.now() - timedelta(days=1)
        json_data = {
            "start_time": yesterday.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        resp = requests.get(self.url+uri, headers=self.header, data=json_data).json()
        return [data['id'] for data in resp.get('data', [])]

    def get_likes(self, id):
        return self.get_tweetfields(id, "public_metrics")["data"][0]["public_metrics"]["like_count"]

    def get_parent_tweet(self, id):
        return self.get_tweetfields(id, "referenced_tweets")["data"][0]["referenced_tweets"][0]["id"]

    def already_replied(self, id):
        uri = "tweets/search/recent"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        json_data = {
            'query': f'in_reply_to_tweet_id:{id} from:YoWhatsTheRatio'
        }
        resp = requests.get(self.url+uri, headers=headers, data=json_data)
        try:
           return resp.json()['meta']['result_count']
        except:
            print("Could not check if tweet {} has already been replied to. Something's wrong")
            return True

    def post_reply_tweet(self, text, parent_id):
        self.refresh_token()
        uri = "tweets"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        json_data = {
            'text': f'{text}',
            'reply': {
                'in_reply_to_tweet_id': f'{parent_id}',
            }
        }
        resp = requests.post(self.url+uri, headers=headers, json=json_data)
        return resp.json()

    def get_tweetfields(self, id, tweetfields="public_metrics"):
        uri = "tweets?ids={}&tweet.fields={}".format(id, tweetfields)
        resp = requests.get(self.url+uri, headers=self.header)
        return resp.json()

if __name__ == '__main__':
    tweepy = Twitter()