from flask import Blueprint, request, redirect, url_for, render_template
from injector import inject
from repository.users_interface import UsersInterface
from models.user import User
from views.decorators.authorization import admin_required
from views.decorators.authorization import admin_or_owner_required
from views.decorators.setup_required import setup_required


users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')

@inject
@users_blueprint.route('/first_login_setup/<int:user_id>', methods=["GET", "POST"])
@setup_required
def first_login_setup(users: UsersInterface, user_id):
    user_to_edit = users.get_user_by_id(user_id)
    if request.method == "GET":
        return render_template('first_login_form.html')
    new_email = request.form['email']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    if new_password == confirm_password:
        users.edit(user_to_edit, user_to_edit.name, new_email, new_password)
        return redirect(url_for('users_blueprint.view_user', user_id=user_to_edit.user_id))
    return None


@inject
@users_blueprint.route('/add', methods=["GET", "POST"])
@setup_required
@admin_required
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
@users_blueprint.route('/edit/<int:user_id>', methods=["GET", "POST"])
@setup_required
@admin_or_owner_required
def edit_user(users: UsersInterface, user_id):
    user_to_edit = users.get_user_by_id(user_id)
    if request.method == "GET":
        return render_template('edit_user.html', user_to_edit=user_to_edit)
    new_name = request.form['name']
    new_email = request.form['email']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    if new_password == confirm_password:
        users.edit(user_to_edit, new_name, new_email, new_password)
        return redirect(url_for('users_blueprint.view_user', user_id=user_to_edit.user_id))
    return None


@inject
@users_blueprint.route('/delete/<int:user_id>')
@setup_required
@admin_required
def delete_user(users: UsersInterface, user_id):
    users.delete(user_id)
    return redirect(url_for('users_blueprint.view_all_users'))


@inject
@users_blueprint.route('/view')
@setup_required
@admin_required
def view_all_users(users: UsersInterface):
    return render_template('list_users.html', users=users.get_all_users())


@inject
@users_blueprint.route('/view/<int:user_id>')
@setup_required
@admin_or_owner_required
def view_user(users: UsersInterface, user_id):
    user_to_view = users.get_user_by_id(user_id)
    return render_template('view_user.html', user=user_to_view)
