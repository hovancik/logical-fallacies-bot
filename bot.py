import praw
import json
import time
from tinydb import TinyDB, Query
from tinydb_serialization import SerializationMiddleware
from serializers import DateTimeSerializer
from datetime import datetime

serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

DB_FILE = './data/db.json'
FALLACIES_FILE = './data/fallacies.json'


def reply_text_for(fallacy):
    """Construct the reply of bot for specific fallacy."""
    reply = "### [" + fallacy['title'] + "]" + "(" + fallacy['link'] + ")\n" + \
        fallacy['text'] + "\n#### Example: \n" + fallacy['example'] + "\n\n" + \
        "*** \nHi, I'm bot. You can find more about me [here](https://fallacy.in/about.html)."
    return reply.replace("<br/>", "\n\n")


def has_reply_on(comment):
    """Check whether the bot has already replied to the Reddit comment"""
    with TinyDB(DB_FILE, storage=serialization) as db:
        Comment = Query()
        return db.contains(Comment.id == comment.id)


def set_as_replied_to(comment, fallacy):
    """Save the Reddit comment's id and current UTC time to the DB to mark it as replied to"""
    with TinyDB(DB_FILE, storage=serialization) as db:
        db.insert({'id': comment.id, 'created_at': datetime.utcnow(),
                   'subreddit': comment.subreddit.display_name, 'fallacy_uid': fallacy['uid']})


def handle_ratelimit(func):
    """Rerun replying to comment if it fails because of RATELIMIT"""
    def wrapper(*args, **kwargs):
        while True:
            try:
                func(*args, **kwargs)
                break
            except praw.exceptions.APIException as error:
                if error.error_type == "RATELIMIT":
                    print("Hit rate limit - Sleeping for 10 minutes.")
                    print(error)
                    time.sleep(60 * 10)
                else:
                    raise
    return wrapper


@handle_ratelimit
def bot_reply(comment, fallacy):
    """Handle newly found comment by replying to it and setting as replied to"""
    print("found comment " + comment.id + ": " + comment.body)
    comment.reply(reply_text_for(fallacy))
    set_as_replied_to(comment, fallacy)


def main():
    reddit = praw.Reddit(
        'fallacybot', user_agent='fallacy.in bot by /u/hovancik')
    subreddit = reddit.subreddit('fallacybottest')

    with open(FALLACIES_FILE, 'r') as f:
        fallacies = json.loads(f.read())

    starters = ["what is ", "what's ", "explain ", "fallacy in "]

    for comment in subreddit.stream.comments():
        normalized_comment = comment.body.lower()
        for starter in starters:
            for fallacy in fallacies:
                normalized_fallacy = fallacy['title'].lower()
                if starter + normalized_fallacy in normalized_comment:
                    if not has_reply_on(comment):
                        if not comment.archived:
                            bot_reply(comment, fallacy)


if __name__ == '__main__':
    main()
