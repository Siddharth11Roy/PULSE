from app import create_app,db
from app.models import *
from app.models import User, Interest, Event
import datetime
import os
from app.models.user import User
from app.models.event import Event
from app.models.interest import Interest
from datetime import datetime
app=create_app()


DB_PATH = 'community.db'  # or use app.config['SQLALCHEMY_DATABASE_URI'].split:///[-1]



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        user = User.query.filter_by(phone="1234567890").first()
        if not user:
            user = User(
                username="john_doe",
                email="john@example.com",
                phone="1234567890",
                password="test123"
            )
            db.session.add(user)
            db.session.commit()
            print(f"User created: {user}")

        event=Event.query.filter_by(title="Local Cricket Match").first()
        if not event:
            event = Event(
                title="Local Cricket Match",
                description="A fun Sunday cricket match at the park.",
                location="Greenfield Park, Sector 21",
                category="Sports Match",
                date=datetime(2025, 5, 25, 10, 0),
                user_id=user.id
            )
            db.session.add(event)
            db.session.commit()
            print(f"Event created: {event}")

        interest = Interest.query.filter_by(name="Alice").first()
        if not interest:
            interest = Interest(
                name="Alice",
                email="alice@example.com",
                phone="9876543210",
                people_count=2,
                user_id=user.id,
                event_id=event.id
            )
            db.session.add(interest)
            db.session.commit()
            print(f"Interest created: {interest}")
        
        
        app.run(debug=True)