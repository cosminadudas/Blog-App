from flask import Blueprint, request, redirect, render_template
from injector import inject
from setup.config_interface import ConfigInterface
from setup.database_setup import DatabaseSetup
from models.database_setup_model import DatabaseSetupModel
from repository.blog_posts_database_repository import COMMAND

setup_blueprint = Blueprint('setup_blueprint', __name__)
database_config: ConfigInterface

@inject
@setup_blueprint.route('/setup', methods=["GET", "POST"])
def db_setup(database_config: ConfigInterface):
    if database_config.is_configured:
        return redirect('/home')
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        database = request.form['database']
        db_setup = DatabaseSetupModel('postgresql', 'localhost', user, password, database)
        setup = DatabaseSetup()
        setup.create_database(database, user, password)
        setup.create_table(COMMAND)
        database_config.save_credentials(db_setup)
        return redirect('/home')
    return render_template('setup_db.html')
    