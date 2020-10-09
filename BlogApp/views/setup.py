from flask import Blueprint, request, redirect, render_template
from injector import inject
from setup.database_config import DatabaseConfig
from setup.database_setup import DatabaseSetup
from models.database_credentials import DatabaseCredentials

setup_blueprint = Blueprint('setup_blueprint', __name__)

@inject
@setup_blueprint.route('/setup', methods=["GET", "POST"])
def db_setup(database_config: DatabaseConfig):
    if database_config.is_configured:
        return redirect('/home')
    if request.method == "POST":
        database_credentials = DatabaseCredentials(request.form['user'],
                                                   request.form['password'],
                                                   request.form['database'])
        database_config.save_credentials(database_credentials)
        setup = DatabaseSetup()
        setup.create_database()
        return redirect('/home')
    return render_template('setup_db.html')
    