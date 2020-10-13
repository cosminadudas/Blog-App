from flask import redirect

class SetupManager:

    @staticmethod
    def get_setup_status(database_config):
        if not database_config.is_configured:
            return redirect('/setup')
        return None
