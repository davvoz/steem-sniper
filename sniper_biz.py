import time
import logging
from datetime import datetime, timedelta
import threading
from beem import Steem
from beem.account import Account
from beem.exceptions import AccountDoesNotExistsException, VotingInvalidOnArchivedPost
from beem.comment import Comment
from beem.imageuploader import ImageUploader
import queue
import json

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AuthorConfig:
    def __init__(self, vote_percentage=50, post_delay_minutes=1, daily_vote_limit=5, 
                 add_comment=True, add_image=True, comment_text="", image_path=""):
        self.vote_percentage = vote_percentage
        self.post_delay_minutes = post_delay_minutes
        self.daily_vote_limit = daily_vote_limit
        self.add_comment = add_comment
        self.add_image = add_image
        self.comment_text = comment_text
        self.image_path = image_path
        self.votes_today = 0
        self.last_vote_time = None
        self.insert_at_now = datetime.now()
        self.log_queue = queue.Queue()

    def can_vote(self):
        now = datetime.now()
        if self.last_vote_time is None or now.date() > self.last_vote_time.date():
            self.votes_today = 0
        return self.votes_today < self.daily_vote_limit and self.insert_at_now <= now

    def record_vote(self):
        self.votes_today += 1
        self.last_vote_time = datetime.now()
        

class SteemSniperBackend:
    def __init__(self):
        self.steem = None
        self.running = False
        self.config = {
            'posting_key': '',
            'voter': '',
            'interval': 20,  # intervallo di polling in secondi
        }
        self.author_configs = {}
        self.lock = threading.Lock()
        #queue per i log
        self.log_queue = queue.Queue()

    def get_logs(self):
        logs = []
        while not self.log_queue.empty():
            logs.append(self.log_queue.get())
        return logs

    def log(self, message, level='INFO'):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        self.log_queue.put(json.dumps(log_entry))
    
    def configure(self, **kwargs):
        """Update global configuration with provided values."""
        self.config.update(kwargs)

    def configure_author(self, author, **kwargs):
        """Configure or update settings for a specific author."""
        if author not in self.author_configs:
            self.author_configs[author] = AuthorConfig()
        for key, value in kwargs.items():
            setattr(self.author_configs[author], key, value)

    def setup_steem_client(self):
        """Set up and return a Steem client."""
        try:
            self.steem = Steem(node="https://api.steemit.com", keys=[self.config['posting_key']])
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Steem node: {str(e)}")
            self.log("Failed to connect to Steem node", "ERROR")
            return False

    def validate_author(self, author):
        """Validate if an author exists on Steem."""
        try:
            Account(author, blockchain_instance=self.steem)
            return True
        except AccountDoesNotExistsException:
            logger.error(f"Invalid target: {author}")
            self.log("Invalid target: {author}", "ERROR")

            return False

    def get_latest_post(self, author):
        """Get the latest post of an author."""
        try:
            account = Account(author, blockchain_instance=self.steem)
            posts = account.get_blog(limit=1)
            return posts[0] if posts else None
        except Exception as e:
            self.log(f"Error retrieving latest post for {author}: {str(e)}", "ERROR")
            return None

    def has_already_voted(self, post, voter):
        """Check if the voter has already voted on the post."""
        votes = post.get_votes()
        return any(vote['voter'] == voter for vote in votes)

    def upload_image(self, image_path, voter):
        """Upload an image and return the URL."""
        try:
            uploader = ImageUploader(blockchain_instance=self.steem)
            account = Account(voter, blockchain_instance=self.steem)
            image_url = uploader.upload(image_path, account.name)
            if isinstance(image_url, dict) and 'url' in image_url:
                return image_url['url']
            else:
                self.log(f"Image upload failed: {image_url}", "ERROR")
                return None
        except Exception as e:
            self.log(f"Error uploading image: {str(e)}", "ERROR")
            return None

    def comment_post(self, post, author_config):
        """Add a comment to a post based on author configuration."""
        try:
            voter_account = Account(self.config['voter'], blockchain_instance=self.steem)
            comment = Comment(post, blockchain_instance=self.steem)
            
            comment_body = author_config.comment_text
            if author_config.add_image and author_config.image_path:
                image_url = self.upload_image(author_config.image_path, self.config['voter'])
                if image_url:
                    comment_body += f"\n\n![image]({image_url})"
                else:
                    self.log("Failed to upload image for comment", "ERROR")
            
            comment.reply(body=comment_body, author=voter_account.name)
            return True
        except Exception as e:
            self.log(f"Error commenting on post: {str(e)}", "ERROR")
            return False

    def upvote_post(self, post, author):
        """Upvote a post and optionally add a comment based on author configuration."""
        author_config = self.author_configs[author]
        try:
            voter_account = Account(self.config['voter'], blockchain_instance=self.steem)
            if self.has_already_voted(post, voter_account.name):
                self.log(f"Already voted on post: {post.title}", "INFO")
                return False
            
            if not author_config.can_vote():
                self.log(f"Daily vote limit reached for {author}", "INFO")
                return False

            post.upvote(weight=author_config.vote_percentage, voter=voter_account.name)
            self.log(f"Upvoted post: {post.title} by {author}", "INFO")
            author_config.record_vote()

            if author_config.add_comment:
                self.comment_post(post, author_config)

            return True
        except VotingInvalidOnArchivedPost:
            self.log(f"Post is too old to be voted on: {post.title}", "INFO")
            return False
        except Exception as e:
            self.log(f"Error upvoting post: {str(e)}", "ERROR")
            return False

    def get_post_creation_time(self, post):
        """Get the creation time of a post."""
        return post['created']

    def run_upvote_for_author(self, author, config):
        """Run upvoting process for a specific author."""
        if not self.validate_author(author):
            return

        latest_post = self.get_latest_post(author)
        if latest_post:
            current_time = datetime.utcnow()
            post_time = self.get_post_creation_time(latest_post)
            post_age = (current_time - post_time.replace(tzinfo=None)).total_seconds() / 60  # Convert to minutes

            logger.info(f"New post detected for {author}: {latest_post.permlink}")
            self.log(f"New post detected for {author}: {latest_post.permlink}", "INFO")
            logger.info(f"Post age: {post_age:.2f} minutes")
            self.log(f"Post age: {post_age:.2f} minutes", "INFO")

            if post_age >= config.post_delay_minutes:
                self.upvote_post(latest_post, author)
            else:
                logger.info(f"Post by {author} is too recent. Will check again in next cycle.")
                self.log(f"Post by {author} is too recent. Will check again in next cycle.", "INFO")
        else:
            logger.info(f"No post available for '{author}'.")
            self.log(f"No post available for '{author}'.", "INFO")

    def run_upvote(self):
        """Main loop for sniping posts."""
        if not self.setup_steem_client():
            return

        while self.running:
            for author, config in self.author_configs.items():
                if not self.running:
                    break
                self.run_upvote_for_author(author, config)

            logger.info(f"Reloading... Next check in {self.config['interval']} seconds.")
            self.log(f"Reloading... Next check in {self.config['interval']} seconds.", "INFO")
            time.sleep(self.config['interval'])  # breve intervallo tra i cicli

        logger.info("Sniper operation completed.")
        self.log("Sniper operation completed.", "INFO")

    def start(self):
        """Start the sniping process."""
        if self.running:
            logger.warning("Sniper is already running!")
            self.log("Sniper is already running!", "WARNING")
            return

        self.running = True
        main_thread = threading.Thread(target=self.run_upvote)
        main_thread.start()

    def stop(self):
        """Stop the sniping process."""
        self.running = False
        logger.info("Stopping sniper...")
        self.log("Stopping sniper...", "INFO")
