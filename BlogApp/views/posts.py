from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, session, abort
from injector import inject
from views.my_decorators.login_required import login_required
from models.blog_post import BlogPost
from repository.blog_posts_interface import BlogPostsInterface
from setup.database_config import DatabaseConfig


blog_blueprint = Blueprint('blog_blueprint', __name__)

@inject
@blog_blueprint.before_request
def get_setup_status(database_config: DatabaseConfig):
    if not database_config.is_configured:
        return redirect('/setup')
    return None


@inject
@blog_blueprint.route('/home')
@blog_blueprint.route('/posts')
@blog_blueprint.route('/')
def index(blog_posts: BlogPostsInterface):
    return render_template('list_posts.html', posts=blog_posts.get_all_posts())

@inject
@blog_blueprint.route('/add/post', methods=["GET", "POST"])
@login_required
def add_post(blog_posts: BlogPostsInterface):
    if request.method == "POST":
        new_post = BlogPost(0, '', '', '')
        new_post.title = request.form['title']
        new_post.content = request.form['content']
        new_post.created_at = datetime.now()
        blog_posts.add(new_post)
        return redirect(url_for('blog_blueprint.view_post',
                                post_id=new_post.post_id))
    return render_template('create_post.html')


@inject
@blog_blueprint.route('/edit/post/<int:post_id>', methods=["GET", "POST"])
@login_required
def edit_post(blog_posts: BlogPostsInterface, post_id):
    post_to_edit = blog_posts.get_post_by_id(post_id)
    if post_to_edit.owner != session['id'] and session['username'] != 'admin':
        return abort(403)
    if request.method == "POST":
        new_title = request.form['title']
        new_content = request.form['content']
        blog_posts.edit(post_id, new_title, new_content)
        return redirect(url_for('blog_blueprint.view_post', post_id=post_to_edit.post_id))
    return render_template('edit_post.html', post_to_edit=post_to_edit)


@inject
@blog_blueprint.route('/delete/post/<int:post_id>', methods=["GET", "POST"])
@login_required
def delete_post(blog_posts: BlogPostsInterface, post_id):
    post_to_delete = blog_posts.get_post_by_id(post_id)
    if post_to_delete.owner != session['id'] and session['username'] != 'admin':
        return abort(403)
    blog_posts.delete(post_id)
    return redirect(url_for('blog_blueprint.index'))


@inject
@blog_blueprint.route('/view/post/<int:post_id>')
def view_post(blog_posts: BlogPostsInterface, post_id):
    post_to_view = blog_posts.get_post_by_id(post_id)
    return render_template('view_post.html',
                           post=post_to_view)
