from flask import Flask
from flask_injector import FlaskInjector
from views.posts import blog_blueprint
from views.setup import setup_blueprint
from services.production_dependencies import production_configure

app = Flask(__name__)
app.register_blueprint(setup_blueprint)
app.register_blueprint(blog_blueprint)

FlaskInjector(app=app, modules=[production_configure])

if __name__ == '__main__':
# Run the app server on localhost:4449
    app.run('localhost', 4449)
