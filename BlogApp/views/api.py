from flask import Blueprint, jsonify, abort
from injector import inject
from repository.blog_posts_interface import BlogPostsInterface

api_blueprint = Blueprint("api_blueprint", __name__)


@inject
@api_blueprint.route('/API/post/<post_id>')
def api_post_view(post_id, blog_posts: BlogPostsInterface):
    post = blog_posts.get_post_by_id(post_id)
    if post is None:
        return abort(404)
    return jsonify({
        'title': post.title,
        'owner': post.owner,
        'content': post.content,
        'image': post.image,
        "created_at": '{}/{}/{}'.format(post.created_at.day, post.created_at.month, post.created_at.year),
        "modified_at": post.modified_at
    })
