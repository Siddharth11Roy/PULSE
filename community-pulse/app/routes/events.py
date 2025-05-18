from flask import Blueprint, render_template

@events_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        new_event = Event(
            title=request.form['title'],
            description=request.form['description'],
            category=request.form['category'],
            location=request.form['location'],
            event_date=request.form['event_date']
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('event.list_events'))
    return render_template('create_event.html')


@events_bp.route('/')
def list_events():
    events = Event.query.all()
    return render_template('event_list.html', events=events)


@events_bp.route('/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

