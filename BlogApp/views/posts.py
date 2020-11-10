from datetime import datetime
from exceptions import FormatFileNotAccepted
from flask import Blueprint, request, redirect, url_for, render_template, session, abort
from injector import inject
from views.decorators.setup_required import setup_required
from views.decorators.authorization import login_required
from models.blog_post import BlogPost
from models.pagination import Pagination
from repository.blog_posts_interface import BlogPostsInterface
from repository.users_interface import UsersInterface


blog_blueprint = Blueprint('blog_blueprint', __name__)


@inject
@blog_blueprint.route('/')
@blog_blueprint.route('/home')
@blog_blueprint.route('/posts')
@setup_required
def index(blog_posts: BlogPostsInterface, users: UsersInterface):
    pagination = Pagination(0, 1)
    count_posts = blog_posts.count(request.args.get('user'))
    if count_posts == 0 or count_posts < 5:
        pagination.last_page = 0
    elif count_posts % pagination.limit != 0:
        pagination.last_page = int(count_posts/pagination.limit)
    else:
        pagination.last_page = int(count_posts/pagination.limit - 1)
    current_page = request.args.get('page')
    if current_page is not None:
        if int(current_page) < 0 or int(current_page) > pagination.last_page:
            pagination.page_number = 0
        else:
            pagination.page_number = int(request.args.get('page'))
    return render_template('list_posts.html',
                           users=users.get_all_users(),
                           posts=blog_posts.get_all_posts(request.args.get('user'), pagination),
                           query=request.args.get('user'),
                           pagination=pagination)


@inject
@blog_blueprint.route('/add', methods=["GET", "POST"])
@setup_required
@login_required
def add_post(blog_posts: BlogPostsInterface):
    if request.method == "POST":
        new_post = BlogPost(0, '', '', '', '')
        if request.files:
            new_post.image = request.files["image"]
        new_post.owner = session['id']
        new_post.title = request.form['title']
        new_post.content = request.form['content']
        new_post.created_at = datetime.now()
        try:
            blog_posts.add(new_post)
        except FormatFileNotAccepted:
            return render_template('create_post.html',
                                   error='File format not accepted. Try again with new file!')
        return redirect(url_for('blog_blueprint.view_post',
                                post_id=new_post.post_id))
    return render_template('create_post.html')


@inject
@blog_blueprint.route('/edit/<int:post_id>', methods=["GET", "POST"])
@setup_required
@login_required
def edit_post(blog_posts: BlogPostsInterface, post_id):
    post_to_edit = blog_posts.get_post_by_id(post_id)
    if post_to_edit.owner != session['username'] and session['username'] != 'admin':
        return abort(403)
    if request.method == "POST":
        image = ''
        if request.files:
            image = request.files["image"]
        new_title = request.form['title']
        new_content = request.form['content']
        try:
            blog_posts.edit(post_id, new_title, new_content, image)
        except FormatFileNotAccepted:
            return render_template('edit_post.html',
                                   post_to_edit=post_to_edit,
                                   error='File format not accepted. Try again with new file!')
        return redirect(url_for('blog_blueprint.view_post', post_id=post_to_edit.post_id))
    return render_template('edit_post.html', post_to_edit=post_to_edit)


@inject
@blog_blueprint.route('/delete/<int:post_id>', methods=["GET", "POST"])
@setup_required
@login_required
def delete_post(blog_posts: BlogPostsInterface, post_id):
    post_to_delete = blog_posts.get_post_by_id(post_id)
    if post_to_delete.owner != session['username'] and session['username'] != 'admin':
        return abort(403)
    blog_posts.delete(post_id)
    return redirect(url_for('blog_blueprint.index'))


@inject
@blog_blueprint.route('/view/<int:post_id>')
@setup_required
def view_post(blog_posts: BlogPostsInterface, post_id):
    post_to_view = blog_posts.get_post_by_id(post_id)
    return render_template('view_post.html',
                           post=post_to_view)
