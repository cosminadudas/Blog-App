from flask import Blueprint, request, redirect, url_for, render_template, session
from injector import inject
from repository.users_interface import UsersInterface
from models.user import User
from setup.database_config import DatabaseConfig

users_blueprint = Blueprint('users_blueprint', __name__)

@inject
@users_blueprint.before_request
def get_setup_status(database_config: DatabaseConfig):
    if not database_config.is_configured:
        return redirect('/setup')
    return None



@users_blueprint.before_request
def is_admin_logged_in():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] != 'admin':
        return redirect('/login')
    return None


@inject
@users_blueprint.route('/add/user', methods=["GET", "POST"])
def add_user(users: UsersInterface):
    if request.method == "POST":
        new_user = User(0, '', '', '')
        new_user.name = request.form['name']
        new_user.email = request.form['email']
        new_user.password = request.form['password']
        users.add(new_user)
        return redirect(url_for('users_blueprint.view_user', user_id=new_user.user_id))
    return render_template('create_user.html')


@inject
@users_blueprint.route('/edit/user/<int:user_id>', methods=["GET", "POST"])
def edit_user(users: UsersInterface, user_id):
    user_to_edit = users.get_user_by_id(user_id)
    if request.method == "POST":
        new_name = request.form['name']
        new_email = request.form['email']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if new_password == confirm_password:
            users.edit(user_id, new_name, new_email, new_password)
            return redirect(url_for('users_blueprint.view_user', user_id=user_to_edit.user_id))
    return render_template('edit_user.html', user_to_edit=user_to_edit)


@inject
@users_blueprint.route('/delete/user/<int:user_id>')
def delete_user(users: UsersInterface, user_id):
    users.delete(user_id)
    return render_template('/list_users.html', users=users.get_all_users())


@inject
@users_blueprint.route('/view/users')
def view_all_users(users: UsersInterface):
    return render_template('list_users.html', users=users.get_all_users())


@inject
@users_blueprint.route('/view/user/<int:user_id>')
def view_user(users: UsersInterface, user_id):
    user_to_view = users.get_user_by_id(user_id)
    return render_template('view_user.html', user=user_to_view)
