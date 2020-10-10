from flask import Blueprint, request, redirect, render_template, session
from injector import inject
from repository.users_interface import UsersInterface
from services.password_manager import PasswordManager

login_blueprint = Blueprint('login_blueprint', __name__)

@inject
@login_blueprint.route('/login', methods=['GET', 'POST'])
def user_login(users: UsersInterface):
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        user = users.get_user_by_name_or_email(username_or_email)
        if user is not None:
            hashed_password = PasswordManager.convert_to_hashed_password(password)
            if hashed_password == user.password:
                session['user'] = user.name
                session['id'] = user.user_id
                return redirect('/home')
            return render_template('login.html', error='Wrong password!Try again!')
        return render_template('login.html', error='Wrong email or username!Try again!')
    return render_template('login.html')
