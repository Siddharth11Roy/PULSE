from flask import Blueprint, render_template

event_bp = Blueprint('event', __name__, url_prefix='/events')

@event_bp.route('/<int:event_id>')
def event_detail(event_id):
    # You can fetch event details from DB here using `event_id`
    return render_template('event_detail.html', event_id=event_id)
