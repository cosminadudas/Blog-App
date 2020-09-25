from datetime import datetime


class BlogPost:
    def __init__(self, post_id, owner, title, content):
        self.post_id = post_id
        self.owner = owner
        self.title = title
        self.content = content
        self.created_at = self.modified_at = datetime.now()


    def preview_content(self):
        return self.content[:15] + '[...]'
