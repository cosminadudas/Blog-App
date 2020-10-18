from exceptions import LoginError, UserNotSetupError
from flask import Blueprint, request, redirect, render_template
from injector import inject
from services.authentication import Authentication
from views.decorators.setup_required import setup_required


login_blueprint = Blueprint('login_blueprint', __name__)


@inject
@login_blueprint.route('/login', methods=['GET', 'POST'])
@setup_required
def user_login(authentication: Authentication):
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']
        try:
            authentication.login(username_or_email, password)
            return redirect('/home')
        except UserNotSetupError:
            return render_template('first_login_form.html', user_to_edit=authentication.user)
        except LoginError:
            error = "Wrong username/email or password! Try again!"
            return render_template('login.html', error=error)
    return render_template('login.html')



@inject
@login_blueprint.route('/logout')
@setup_required
def user_logout(authentication: Authentication):
    authentication.logout()
    return redirect('/home')
