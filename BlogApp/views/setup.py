import os
from flask import Blueprint, request, redirect, render_template
from database_setup.database import Database

setup_blueprint = Blueprint('setup_blueprint', __name__)
database_setup = Database()

@setup_blueprint.route('/setup', methods=["GET", "POST"])
def db_setup():
    if os.path.exists('database_setup/database.ini'):
        return redirect('/home')
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        database = request.form['database']
        database_setup.credentials.save_credentials(user, password, database)
        database_setup.create_database(database, user, password)
        return redirect('/home')
    return render_template('setup_db.html')
    