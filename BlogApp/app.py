from flask import Flask
from views.posts import blog_blueprint
from views.setup import setup_blueprint

app = Flask(__name__)
app.register_blueprint(setup_blueprint)
app.register_blueprint(blog_blueprint)


if __name__ == '__main__':
# Run the app server on localhost:4449
    app.run('localhost', 4449)
