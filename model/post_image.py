
class PostImage(dict):
    def __init__(self, post_id, file_name, file_hash, time_created):
        dict.__init__(self, post_id=post_id, file_name=file_name, file_hash=file_hash, time_created=time_created)
