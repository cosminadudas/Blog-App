from flask import render_template, url_for, request, redirect
from datetime import datetime
from models import BlogPost

class Posts(object):
    posts: list
    def __init__(self, posts):
        self.posts = posts
        self.index = 0

    def __iter__(self):
        return iter(self.posts)


    def __next__(self):
        if self.index < len(posts):
            result = self.posts[self.index]
        self.index += 1
        return result
        raise StopIteration

    def add(self, new_post : BlogPost, method):
        if (method == "POST"):
            new_post.id = len(self) + 1
            new_post.title = request.form['title']
            new_post.content = request.form['content']
            new_post.owner = request.form['owner']
            new_post.created_at = datetime.now()
            self.append(new_post)
            return redirect(url_for('home'))
        return render_template('create_post.html')

    def edit(self, post_id, method):
        post_to_edit = BlogPost()
        for post in self:
            if post.id == post_id:
                post_to_edit = post
        if request.method == "POST":
            post_to_edit.title = request.form['title']
            post_to_edit.content = request.form['content']
            post_to_edit.modified_at = datetime.now()
            return redirect(url_for('home'))
        return render_template('edit_post.html', post_to_edit = post_to_edit)


    def delete(post_id):
        post_to_delete = BlogPost()
        for post in posts:
            if post.id == post_id:
                post_to_delete = post
        self.remove(post_to_delete)
        return redirect(url_for('home'))


    def post(post_id):
        post_to_view = BlogPost()
        for post in self:
            if post.id == post_id:
                post_to_view = post
        return render_template('post.html', post = post_to_view)


