from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import db
from app.models.interest import Interest
from app.models.event import Event
import requests
from flask_login import login_required, current_user
from datetime import datetime
# Blueprint for events
events_bp = Blueprint('event', __name__, url_prefix='/events')

# Route to create a new event
@events_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        new_event = Event(
            title=request.form['title'],
            description=request.form['description'],
            category=request.form['category'],
            location=request.form['location'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
            user_id=current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('event.list_events'))
    return render_template('create_events.html')

# 🛠 Fixed: Route to browse all events
@events_bp.route('/')
def list_events():
    return render_template('events.html')  # Your simple page with a register button

# Route for a specific event's detail page
@events_bp.route('/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

# Route to register interest in an event
@events_bp.route('/<int:event_id>/register', methods=['POST'])
@login_required
def register_interest(event_id):
    name = request.form['name']
    email = request.form['email']
    phone = request.form.get('phone')
    guests = request.form.get('guests', 0)

    interest = Interest(
        name=name,
        email=email,
        phone=phone,
        guests=int(guests),
        event_id=event_id
    )
    db.session.add(interest)
    db.session.commit()

    flash('Thanks for registering! You’ll get updates soon.')
    return redirect(url_for('event.event_detail', event_id=event_id))


@events_bp.route('/nearby')
def nearby_events():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if not lat or not lng:
        return "Location not found", 400

    # Reverse geocode lat/lng using OpenCage, Nominatim, etc.
    # Here’s a basic example with OpenStreetMap’s Nominatim API
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}"
    try:
        geo_response = requests.get(url, headers={"User-Agent": "community-pulse"}).json()
        city = geo_response.get('address', {}).get('city') or \
               geo_response.get('address', {}).get('town') or \
               geo_response.get('address', {}).get('village') or \
               geo_response.get('address', {}).get('state')

        if not city:
            return "Could not determine location", 404

        # Search events matching the location
        events = Event.query.filter(Event.location.ilike(f"%{city}%")).all()

        return render_template('partials/event_cards.html', events=events, location=city)

    except Exception as e:
        return f"Error: {str(e)}", 500
    
    