from flask import Blueprint, request, redirect, render_template
from injector import inject
from repository.users_interface import UsersInterface
from setup.database_config import DatabaseConfig
from services.auth_manager import AuthManager
from services.setup_manager import SetupManager

login_blueprint = Blueprint('login_blueprint', __name__)

@inject
@login_blueprint.before_request
def get_setup_status(database_config: DatabaseConfig):
    return SetupManager.get_setup_status(database_config)


@inject
@login_blueprint.route('/login', methods=['GET', 'POST'])
def user_login(users: UsersInterface):
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        user = users.get_user_by_name_or_email(username_or_email)
        try:
            AuthManager.login(user, password)
            return redirect('/home')
        except SyntaxError:
            error = "Wrong username/email or password! Try again!"
            return render_template('login.html', error=error)
    return render_template('login.html')


@inject
@login_blueprint.route('/logout')
def user_logout():
    AuthManager.logout()
    return redirect('/home')
