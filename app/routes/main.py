from flask import Blueprint, render_template, current_app
from datetime import datetime

# Blueprint oluştur
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Ana sayfa."""
    return render_template('index.html')

@bp.route('/about')
def about():
    """Hakkında sayfası."""
    return render_template('about.html')

@bp.context_processor
def utility_processor():
    """Template değişkenleri."""
    return {
        'now': datetime.now()
    } 