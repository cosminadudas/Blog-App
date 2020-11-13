from models.statistics import Statistics

class UserStatistics:

    def __init__(self, posts, users):
        self.users = users
        self.posts = posts
        self.user_posts = None

    def get_statistics(self):
        all_statistics = []
        for user in self.users.get_all_users():
            self.user_posts = self.posts.get_all_posts(user.name, None)
            user = user.name
            active_months = self.get_active_months()
            user_statistics = Statistics(user, active_months)
            all_statistics.append(user_statistics)
        return all_statistics

    def get_posts_count(self, month):
        count = 0
        for post in self.user_posts:
            if post.created_at.strftime('%B') == month:
                count += 1
        return count

    def get_active_months(self):
        active_months = []
        for post in self.user_posts:
            active_month = post.created_at.strftime('%B')
            if active_months != [] and active_month in active_months[0]:
                pass
            else:
                active_months.append((active_month, ': ' +\
                    str(self.get_posts_count(active_month))+' posts'))
        if active_months == []:
            active_months.append(('', 'No posts yet!'))
        return set(active_months)

    def get_user_posts_ids(self):
        user_posts_ids = []
        for post in self.user_posts:
            user_posts_ids.append(post.post_id)
        return user_posts_ids
