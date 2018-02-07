# logical-fallacies-bot
Reddit bot for [Fallacy.in](https://fallacy.in)

## What does it do?
The main idea of this bot is to explain logical fallacies on Reddit, when invited to do so by some Reddit user.

Users can do it by using [specific wording](https://fallacy.in/about.html) in their comments, eg. `fallacy in appeal to probability`. Bot will reply to that comment with fallacy explanantion. Example can be seen [here](https://www.reddit.com/r/fallacybottest/comments/5w3ujc/test/deq1v95/?context=10000).

## How does it works?
The bot watches comments in specified subreddits and tries to find the match. If match is found, it generates reply based on data provided by it's web companion, [Fallacy.in](https://fallacy.in) website, which is [open-source](https://github.com/hovancik/logical-fallacies) as well.

Data are located [here](https://fallacy.in/data/fallacies.json).

## Code
- praw.ini.example has the data needed to run bot correctly.
- `pipenv run python download.py` downloads data for bot
- `pipenv run python bot.py` runs the bot
