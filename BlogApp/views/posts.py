from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template
from models.BlogPost import BlogPost
from repository.in_memory_data import Posts

blog_posts = Posts()
blog_blueprint = Blueprint('blog_blueprint', __name__)


@blog_blueprint.route('/')
@blog_blueprint.route('/home')
@blog_blueprint.route('/posts')
def index():
    return render_template('list_posts.html', posts=blog_posts)


@blog_blueprint.route('/add', methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        new_post = BlogPost(0, '', '', '', '', '')
        new_post.id = blog_posts.count() + 1
        new_post.title = request.form['title']
        new_post.content = request.form['content']
        new_post.owner = request.form['owner']
        new_post.created_at = datetime.now()
        blog_posts.add(new_post)
        return redirect(url_for('blog_blueprint.index'))
    return render_template('create_post.html')


@blog_blueprint.route('/post/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    post_to_edit = BlogPost(0, '', '', '', '', '')
    for blog_post in blog_posts:
        if blog_post.id == post_id:
            post_to_edit = blog_post
            if request.method == "POST":
                new_title = request.form['title']
                new_content = request.form['content']
                blog_posts.edit(post_to_edit, new_title, new_content)
                return redirect(url_for('blog_blueprint.index'))
    return render_template('edit_post.html', post_to_edit=post_to_edit)


@blog_blueprint.route('/post/delete/<int:post_id>', methods=["GET", "POST"])
def delete_post(post_id):
    post_to_delete = BlogPost(0, '', '', '', '', '')
    for blog_post in blog_posts:
        if blog_post.id == post_id:
            post_to_delete = blog_post
            blog_posts.delete(post_to_delete)
    return redirect(url_for('blog_blueprint.index'))


@blog_blueprint.route('/post/<int:post_id>', methods=["GET", "POST"])
def post(post_id):
    post_to_view = BlogPost(0, '', '', '', '', '')
    for blog_post in blog_posts:
        if blog_post.id == post_id:
            post_to_view = blog_post
    return render_template('view_post.html', post=post_to_view)
