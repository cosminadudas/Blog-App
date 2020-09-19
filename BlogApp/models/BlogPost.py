class BlogPost:
    def __init__(self, id, owner, title, content, created_at, modified_at):
        self.id = id
        self.owner = owner
        self.title = title
        self.content = content
        self.created_at = created_at
        self.modified_at = modified_at

    
    def preview_content(self):
        return self.content[:15] + '...'
