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
    #DEFAULT_AUTHORS = ["maodomy","gue22","aston.villa","Kork75","mia.fobos", "im-ridd", "tasubot", "stefano.massari", "wildnature1", "mikitaly", "guersy", "frafiomatale", "cur8"]

    sniper.configure_author("maodomy", 
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Bel post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    # Configure individual authors
    sniper.configure_author("gue22", 
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Bel post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    sniper.configure_author("aston.villa", 
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=False,
                            comment_text="Bel post!")
    
    sniper.configure_author("Kork75", 
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=False,
                            comment_text="Bel post!")
    
    sniper.configure_author("mia.fobos",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Bel post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    sniper.configure_author("im-ridd",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Bel post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    sniper.configure_author("tasubot",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Bel post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    sniper.configure_author("stefano.massari",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=False,
                            comment_text="Bel post!")
    
    sniper.configure_author("wildnature1",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Bel post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    sniper.configure_author("mikitaly",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=False,
                            comment_text="Bel post!")
    
    sniper.configure_author("guersy",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Bel post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    sniper.configure_author("frafiomatale",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=False,
                            comment_text="Bel post!")
    
    sniper.configure_author("cur8",
                            vote_percentage=75, 
                            post_delay_minutes=1, 
                            daily_vote_limit=30, 
                            add_comment=True, 
                            add_image=True,
                            comment_text="Bel post!",
                            image_path="_0d47c611-0fa1-4df6-898c-b6620812e18d.jpeg")
    
    
    sniper.start()
    # To stop the sniper after some time:
    # time.sleep(300)  # Run for 5 minutes
    # sniper.stop()