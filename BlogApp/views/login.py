from exceptions import LoginError
from flask import Blueprint, request, redirect, render_template
from injector import inject
from repository.users_interface import UsersInterface
from services.authentication_manager import AuthenticationManager
from views.decorators.setup_required import setup_required


login_blueprint = Blueprint('login_blueprint', __name__)


@inject
@login_blueprint.route('/login', methods=['GET', 'POST'])
@setup_required
def user_login(users: UsersInterface):
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        user = users.get_user_by_name_or_email(username_or_email)
        try:
            AuthenticationManager.set_password(users, user, password)
            AuthenticationManager.login(user, password)
            return redirect('/home')
        except LoginError:
            error = "Wrong username/email or password! Try again!"
            return render_template('login.html', error=error)
    return render_template('login.html')


@inject
@login_blueprint.route('/logout')
@setup_required
def user_logout():
    AuthenticationManager.logout()
    return redirect('/home')
