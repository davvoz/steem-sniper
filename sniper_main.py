# Usage example:
from sniper_biz import SteemSniperBackend


if __name__ == "__main__":
    sniper = SteemSniperBackend()
    sniper.configure(
        posting_key="",
        voter="luciojolly",
        interval=1
    )
    
    # Configure individual authors
    sniper.configure_author("fabi.one", 
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Great post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    # Configure individual authors
    sniper.configure_author("gigi.one", 
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=False, 
                            add_image=False)
    
    sniper.start()
    # To stop the sniper after some time:
    # time.sleep(300)  # Run for 5 minutes
    # sniper.stop()