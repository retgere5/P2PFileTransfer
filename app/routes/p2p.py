from flask import Blueprint, render_template, request, abort
import secrets

# Blueprint oluştur
bp = Blueprint('p2p', __name__)

@bp.route('/room')
def room():
    """Oda sayfası."""
    room_id = request.args.get('id')
    
    if room_id:
        # Var olan odaya katıl
        return render_template('p2p/room.html', room_id=room_id)
    else:
        # Yeni oda oluştur
        new_room_id = secrets.token_urlsafe(8)
        return render_template('p2p/room.html', room_id=new_room_id)

@bp.route('/join/<room_id>')
def join_room(room_id):
    """Odaya katıl."""
    if not room_id:
        abort(400)  # Bad Request
    return render_template('p2p/room.html', room_id=room_id) 