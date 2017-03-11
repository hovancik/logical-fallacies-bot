import praw
import json
from tinydb import TinyDB, Query

db = TinyDB('./data/db.json')

reddit = praw.Reddit('fallacybot', user_agent='fallacy.in bot by /u/hovancik')

def reply_text_for(fallacy):
  """Construct the reply of bot for specific fallacy.""" 
  reply =  "## [" + fallacy['title']+ "]" + "(" + fallacy['link'] + ")\n" + \
  fallacy['text'] + "\n#### Example: \n" + fallacy['example'] + "\n\n" + \
  "*** \nHi, I'm bot. You can find more about me [here](https://fallacy.in/about.html)." 
  return reply.replace("<br/>","\n\n")	
  
def has_commented_on(comment):
  Comment = Query()
  return db.contains(Comment.id == comment.id)

def set_as_commented(comment):
  db.insert({'id': comment.id})

f = open('fallacies.json', 'r')
fallacies = json.loads(f.read())
subreddit = reddit.subreddit('fallacybottest')
starters = ["what is ", "what's ", "explain ", "fallacy in "]

for comment in subreddit.stream.comments():
  normalized_comment = comment.body.lower()
  for starter in starters: 
    for fallacy in fallacies:
      normalized_fallacy = fallacy['title'].lower()
      if starter + normalized_fallacy in normalized_comment:
        if not has_commented_on(comment):
           print("found comment " + comment.id + ": " + comment.body)
           comment.reply(reply_text_for(fallacy))
           set_as_commented(comment)

  
