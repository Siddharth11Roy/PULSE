#approval for users :updates the status
#monitor events  :RD for events


from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
from ..models.user import User
from ..models.event import Event
from .. import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    return '<h1>Admin Dashboard</h1>'

@admin_bp.route('/admin/approve/<int:user_id>')
@login_required
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/approve_events/<int:event_id>')
@login_required
def monitor_events(event_id):
    event = Event.query.get_or_404(event_id)
    event.is_verified=True
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

    
   
