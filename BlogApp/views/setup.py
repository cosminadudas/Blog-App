from flask import Blueprint, request, redirect, render_template
from database_setup.database import Database

setup_blueprint = Blueprint('setup_blueprint', __name__)
database_setup = Database()

@setup_blueprint.route('/setup', methods=["GET", "POST"])
def db_setup():
    if database_setup.is_set_up():
        return redirect('/home')
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        database = request.form['database']
        database_setup.credentials.save_credentials(user, password, database)
        return redirect('/home')
    return render_template('setup_db.html')
    