from flask import Blueprint, render_template
from injector import inject
from views.decorators.setup_required import setup_required
from views.decorators.authorization import admin_required
from services.user_statistics import UserStatistics
from repository.blog_posts_interface import BlogPostsInterface
from repository.users_interface import UsersInterface


statistics_blueprint = Blueprint('statistics_blueprint', __name__)

@inject
@statistics_blueprint.route('/statistics')
@setup_required
@admin_required
def view_statistics(posts: BlogPostsInterface, users: UsersInterface):
    user_statistics = UserStatistics(posts, users)
    return render_template('statistics.html', user_statistics=user_statistics.get_statistics())
