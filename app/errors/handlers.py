from flask import current_app, render_template

from app.errors import bp_errors


@bp_errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp_errors.app_errorhandler(500)
def internal_error(error):
    current_app.db.session.rollback()
    return render_template('errors/500.html'), 500
