from .. import db

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(15))
    people_count = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    def __repr__(self):
        return f"<Interest {self.name} for event {self.event_id}>"