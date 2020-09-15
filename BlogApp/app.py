from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)

posts = [
    {
        'id': 1,
        'title': 'post 1',
        'content':'This is the first blog post.',
        'owner' : 'Cosmina',
        'created_at':'September, 15, 2020',
        'modified_at':''
    },
    {
        'id': 2,
        'title': 'post 2',
        'content':'This is the second blog post.',
        'owner' : 'Larisa',
        'created_at':'September, 15, 2020',
        'modified_at':''
    }
]

@app.route('/')
@app.route('/home')
def home():
    # Render the page
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return "About page"


@app.route('/create', methods = ["GET", "POST"])
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


if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
