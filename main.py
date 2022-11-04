from twitter import Twitter

def reply(tweety, id):
    parent_id = tweety.get_parent_tweet(id)
    parent_like_count = tweety.get_likes(parent_id)
    grandparent_id = tweety.get_parent_tweet(parent_id)
    grandparent_like_count = tweety.get_likes(grandparent_id)

    ratio = parent_like_count / grandparent_like_count

    if ratio > 1:
        reply_string = f"Damn son that's a ratio of {ratio} ! 🔥"
    else:
        reply_string = f"Eh, ratio's just {ratio}. Do better next time."

    tweety.post_reply_tweet(reply_string, id)
    print(reply_string)

def main(code=None):
    tweety = Twitter(code)
    mentions = tweety.get_mentions()
    for id in mentions:
        if tweety.already_replied(id):
            print(id, "Already replied. Skipping all")
            break
        try:
            reply(tweety, id)
        except Exception as E:
            print("Could not reply: ", E)

if __name__ == '__main__':
    main()
