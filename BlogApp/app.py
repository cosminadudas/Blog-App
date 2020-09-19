# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring


from flask import Flask
from views.posts import blog_blueprint

app = Flask(__name__)
app.register_blueprint(blog_blueprint)


if __name__ == '__main__':
# Run the app server on localhost:4449
    app.run('localhost', 4449)
