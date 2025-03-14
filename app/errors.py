from flask import render_template
from app import app

@app.errorhandler(400)
def bad_request(error):
    """400 Bad Request hatası için özel sayfa."""
    return render_template('errors/400.html'), 400

@app.errorhandler(401)
def unauthorized(error):
    """401 Unauthorized hatası için özel sayfa."""
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def forbidden(error):
    """403 Forbidden hatası için özel sayfa."""
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found(error):
    """404 Not Found hatası için özel sayfa."""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    """500 Internal Server Error hatası için özel sayfa."""
    return render_template('errors/500.html'), 500 