import praw
import json
from tinydb import TinyDB, Query
from tinydb_serialization import SerializationMiddleware
from serializers import DateTimeSerializer
from datetime import datetime

serialization = SerializationMiddleware()
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

DB_FILE = './data/db.json'


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


def set_as_replied_to(comment):
    """Save the Reddit comment's id and current UTC time to the DB to mark it as replied to"""
    with TinyDB(DB_FILE, storage=serialization) as db:
        db.insert({'id': comment.id, 'created_at': datetime.datetime.utcnow(),
                   'subreddit': comment.subreddit.display_name})


def main():
    reddit = praw.Reddit(
        'fallacybot', user_agent='fallacy.in bot by /u/hovancik')
    subreddit = reddit.subreddit('fallacybottest')

    with open('fallacies.json', 'r') as f:
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
                            print("found comment " +
                                  comment.id + ": " + comment.body)
                            comment.reply(reply_text_for(fallacy))
                            set_as_replied_to(comment)


if __name__ == '__main__':
    main()
