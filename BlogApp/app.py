from flask import Flask, redirect
from flask_injector import FlaskInjector
from views.posts import blog_blueprint
from views.setup import setup_blueprint
from views.login import login_blueprint
from views.users import users_blueprint
from services.dependencies import configure_production

app = Flask(__name__)

app.secret_key = 'randomstring'
app.register_blueprint(setup_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(blog_blueprint)
app.register_blueprint(users_blueprint)

@app.before_first_request
def get_update():
    return redirect('/setup')

FlaskInjector(app=app, modules=[configure_production])

if __name__ == '__main__':
# Run the app server on localhost:4449
    app.run('localhost', 4449)
