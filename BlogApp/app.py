from flask import Flask, render_template, url_for

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


if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
