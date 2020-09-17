from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from views.index import index_blueprint
from models import BlogPost
from repository.in_memory_data import Posts

app = Flask(__name__)
app.register_blueprint(index_blueprint)


@app.route('/about')
def about():
    return "About page"


@app.route('/add', methods = ["GET", "POST"])
def add_post():
    if request.method == "POST":
        new_post = {
        'id': len(posts) + 1,
        'title': request.form['title'],
        'content':request.form['content'],
        'owner' : request.form['owner'],
        'created_at': datetime.now(),
        'modified_at':''
        }
        posts.append(new_post)
        return redirect(url_for('home'))
    return render_template('create_post.html')


@app.route('/post/<int:post_id>/edit', methods = ["GET","POST"])
def edit(post_id):
    post_to_edit ={}
    for post in posts:
        if post['id'] == post_id:
            post_to_edit = post

    if request.method == "POST":
        post_to_edit['title'] = request.form['title']
        post_to_edit['content'] = request.form['content']
        post_to_edit['modified_at'] = datetime.now()
        return redirect(url_for('home'))
        
    return render_template('edit_post.html', post_to_edit = post_to_edit)


@app.route('/post/delete/<int:post_id>')
def delete(post_id):
    post_to_delete ={}
    for post in posts:
        if post['id'] == post_id:
            post_to_delete = post

    posts.remove(post_to_delete)
    return redirect(url_for('home'))


@app.route('/post/<int:post_id>')
def post(post_id):
    post_to_view ={}
    for post in posts:
        if post['id'] == post_id:
            post_to_view = post
    return render_template('post.html', post = post_to_view)


if __name__ == '__main__':
# Run the app server on localhost:4449
    app.run('localhost', 4449)
