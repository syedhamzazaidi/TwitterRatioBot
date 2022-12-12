from twitter import Twitter
from giphy import Giphy
import random

burn_gif_prompts = ['destroyed', 'rekt', 'get rekt', 'lmao burn', 'savage']
oops_gif_prompts = ['oops', 'better luck next time', 'its ok it happens', 'try again', 'git gud']

def reply(tweety, giphy, id):
    parent_id = tweety.get_parent_tweet(id)
    parent_like_count = tweety.get_likes(parent_id)
    grandparent_id = tweety.get_parent_tweet(parent_id)
    grandparent_like_count = tweety.get_likes(grandparent_id)

    if grandparent_like_count == 0:
        ratio = 'infinity'
    ratio = parent_like_count / grandparent_like_count

    if ratio == 'infinity':
        reply_string = f"Ratio is {ratio}. Absolutely. Royally. Owned. Go rethink your entire life. You don't even get a gif"
        gif_url = ''
    if ratio > 1:
        reply_string = f"Damn son that's a ratio of {ratio} ! 🔥"
        gif_url = giphy.gif(random.choice(burn_gif_prompts))
    else:
        reply_string = f"Eh, ratio's just {ratio}. Do better next time."
        gif_url = giphy.gif(random.choice(oops_gif_prompts))

    tweety.post_reply_tweet(reply_string + ' ' + gif_url, id)
    print(reply_string + ' ' + gif_url)

def main(code=None):
    tweety = Twitter(code)
    giphy = Giphy()
    mentions = tweety.get_mentions()
    for id in mentions:
        if tweety.already_replied(id):
            print(id, "Already replied. Skipping all")
            break
        try:
            reply(tweety, giphy, id)
        except Exception as E:
            print("Could not reply: ", E)

if __name__ == '__main__':
    main()
