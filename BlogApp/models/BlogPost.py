# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods


from datetime import datetime


class BlogPost:
    def __init__(self, post_id, owner, title, content):
        self.id = post_id
        self.owner = owner
        self.title = title
        self.content = content
        self.created_at = self.modified_at = datetime.now()


    def preview_content(self):
        return self.content[:15] + '[...]'
