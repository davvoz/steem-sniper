# Steem Sniper Bot

Steem Sniper Bot is a Python-based tool designed to automatically upvote, comment, and interact with posts from specified authors on the Steem blockchain.

## Features

- Automatic upvoting of new posts from configured authors
- Customizable voting weight per author
- Option to add comments to upvoted posts
- Option to include images in comments
- Daily vote limits per author
- Configurable delay before voting on new posts
- Multi-threaded operation for efficient monitoring of multiple authors

## Requirements

- Python 3.6+
- beem library
- Other dependencies (list to be completed based on import statements)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/steem-sniper-bot.git
   cd steem-sniper-bot
   ```

2. Install the required dependencies:
   ```
   pip install beem
   ```
   (Add any other necessary dependencies)

## Configuration

1. Open `config.py` (or the main script file) and set your Steem account details:

   ```python
   sniper.configure(
       posting_key="YOUR_POSTING_KEY",
       voter="YOUR_STEEM_USERNAME",
       interval=1  # Polling interval in seconds
   )
   ```

2. Configure the authors you want to monitor:

   ```python
   sniper.configure_author("author_username", 
                           vote_percentage=75, 
                           post_delay_minutes=1, 
                           daily_vote_limit=30, 
                           add_comment=True, 
                           add_image=True,
                           comment_text="Great post!",
                           image_path="path/to/image.jpg")
   ```

## Usage

Run the bot using:

```
python main.py
```

The bot will start monitoring the specified authors and interact with their posts according to your configuration.

## Caution

- Be careful with your posting key. Never share it or commit it to version control.
- Be mindful of Steem's rules and community guidelines when using bots.
- Excessive bot activity might be seen as spam. Use responsibly.

## Disclaimer

This bot is for educational purposes only. Use at your own risk. The authors are not responsible for any misuse or for any bans or penalties resulting from the use of this bot.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/steem-sniper-bot/issues) if you want to contribute.

