from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template
from views.index import blog_posts
from models.BlogPost import BlogPost


add_blueprint = Blueprint('add_blueprint', __name__)
edit_blueprint = Blueprint('edit_blueprint', __name__)
delete_blueprint = Blueprint('delete_blueprint', __name__)
post_blueprint = Blueprint('post_blueprint', __name__)

@add_blueprint.route('/add', methods=["GET" , "POST"])
def add_post():
    if request.method == "POST":
        new_post = BlogPost(0, '', '', '', '', '')
        new_post.id = blog_posts.count() + 1
        new_post.title = request.form['title']
        new_post.content = request.form['content']
        new_post.owner = request.form['owner']
        new_post.created_at = datetime.now()
        blog_posts.add(new_post)
        return redirect(url_for('index_blueprint.index'))
    return render_template('create_post.html')


@edit_blueprint.route('/post/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    post_to_edit = BlogPost(0, '', '', '', '', '')
    for post in blog_posts:
        if post.id == post_id:
            post_to_edit = post
            if request.method == "POST" :
                new_title = request.form['title']
                new_content = request.form['content']
                blog_posts.edit(post_to_edit, new_title, new_content)
                return redirect(url_for('index_blueprint.index'))
    return render_template('edit_post.html', post_to_edit=post_to_edit)


@delete_blueprint.route('/post/delete/<int:post_id>', methods = ["GET", "POST"])
def delete_post(post_id):
    post_to_delete = BlogPost(0, '', '', '', '', '')
    for post in blog_posts:
        if post.id == post_id:
            post_to_delete = post
            blog_posts.delete(post_to_delete)
    return redirect(url_for('index_blueprint.index'))


@post_blueprint.route('/post/<int:post_id>', methods = ["GET", "POST"])
def post(post_id):
    post_to_view = BlogPost(0, '', '', '', '', '')
    for post in blog_posts:
        if post.id == post_id:
            post_to_view = post
    return render_template('post.html', post = post_to_view)
