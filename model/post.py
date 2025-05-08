
class Post(dict):
    def __init__(self, id, creator, title, city, type, description=None, 
                 like_count=None, collect_count=None, comment_count=None, share_count=None, 
                 spots=None, time_created=None, time_crawl_started=None, time_crawl_completed=None, is_portrait=None):
        dict.__init__(self, id=id, creator=creator, title=title, description=description, 
                        like_count=like_count, collect_count=collect_count, comment_count=comment_count, share_count=share_count,
                        spots=spots, city=city, type=type, 
                        time_created=time_created, time_crawl_started=time_crawl_started, time_crawl_completed=time_crawl_completed,
                        is_portrait=is_portrait)
