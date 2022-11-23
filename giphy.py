import os
import requests
import random

class Giphy():

    def __init__(self):
        self.token = os.environ['GIPHY_TOKEN']
        self.url = 'https://api.giphy.com/v1/gifs/'

    def gif(self, tag):
        uri = "search"
        json_data = {
            "api_key": self.token,
            "q": tag,
            "limit": 1,
            "offset": random.randint(0, 50),
            "lang": "en"
        }
        resp = requests.get(self.url+uri, params=json_data).json()
        return resp['data'][0]['url']

if __name__ == '__main__':
    giphy = Giphy()
    print(giphy.pull_gif('destroyed'))