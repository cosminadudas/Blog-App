from flask import Blueprint, request, redirect, render_template
from injector import inject
from services.config_database_service import ConfigDatabaseService
from setup.database_setup import DatabaseSetup

setup_blueprint = Blueprint('setup_blueprint', __name__)
database_config: ConfigDatabaseService

@inject
@setup_blueprint.route('/setup', methods=["GET", "POST"])
def db_setup(database_config: ConfigDatabaseService):
    if database_config.is_configured():
        return redirect('/home')
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        database = request.form['database']
        database_config.save_credentials('postgresql', user, password, database)
        setup = DatabaseSetup()
        setup.create_database(database, user, password)
        return redirect('/home')
    return render_template('setup_db.html')
    