from flask import Flask
from views.index import index_blueprint
from views.posts import add_blueprint, edit_blueprint, delete_blueprint, post_blueprint

app = Flask(__name__)
app.register_blueprint(index_blueprint)
app.register_blueprint(add_blueprint)
app.register_blueprint(edit_blueprint)
app.register_blueprint(delete_blueprint)
app.register_blueprint(post_blueprint)

if __name__ == '__main__':
# Run the app server on localhost:4449
    app.run('localhost', 4449)
