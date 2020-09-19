# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=no-self-use

from datetime import datetime
from models.BlogPost import BlogPost
from repository.test_posts import posts

class Posts:
    posts: list

    def __init__(self):
        self.posts = posts
        self.index = 0


    def __iter__(self):
        return iter(self.posts)


    def __next__(self):
        if self.index < len(self.posts):
            result = self.posts[self.index]
            self.index += 1
            return result
        raise StopIteration


    def count(self):
        return len(self.posts)


    def add(self, new_post: BlogPost):
        self.posts.insert(0, new_post)


    def edit(self, post_to_edit, new_title, new_content):
        post_to_edit.title = new_title
        post_to_edit.content = new_content
        post_to_edit.modified_at = datetime.now()


    def delete(self, post_to_delete):
        self.posts.remove(post_to_delete)
