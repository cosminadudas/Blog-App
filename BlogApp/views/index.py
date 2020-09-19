from flask import Blueprint, render_template
from repository.in_memory_data import Posts
from models.BlogPost import BlogPost

post_one = BlogPost(1, 'Cosmina', 'post 1', 'This is the first post', 'September, 15, 2020', '-')
post_two = BlogPost(2, 'Larisa', 'post 2', 'This is the second post', 'September 15, 2020', '-')
posts = [post_one, post_two]
blog_posts = Posts(posts)

index_blueprint = Blueprint('index_blueprint', __name__)

@index_blueprint.route('/')
@index_blueprint.route('/home')
@index_blueprint.route('/posts')
def index():
    return render_template('list_posts.html', posts=blog_posts)
