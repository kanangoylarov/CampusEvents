from app.extensions import db
from app.models.event_model import Event


def get_all():
    return Event.query.order_by(Event.date.asc()).all()


def get_by_id(event_id):
    return db.get_or_404(Event, event_id)


def find_by_room_and_date(room_id, event_date, exclude_id=None):
    query = Event.query.filter(
        Event.room_id == int(room_id),
        Event.date == event_date,
    )
    if exclude_id:
        query = query.filter(Event.id != exclude_id)
    return query.all()


def filter_events(org_id=None, date_from=None, date_to=None,
                  time_from=None, time_to=None):
    query = Event.query
    if org_id:
        query = query.filter(Event.organization_id == int(org_id))
    if date_from:
        query = query.filter(Event.date >= date_from)
    if date_to:
        query = query.filter(Event.date <= date_to)
    if time_from:
        query = query.filter(Event.start_time >= time_from)
    if time_to:
        query = query.filter(Event.start_time <= time_to)
    return query.order_by(Event.date.asc()).all()


def find_expired(today, current_time):
    return Event.query.filter(
        db.or_(
            Event.date < today,
            db.and_(
                Event.date == today,
                Event.end_time.isnot(None),
                Event.end_time < current_time,
            )
        )
    ).all()


def save(event):
    db.session.add(event)
    db.session.commit()


def update():
    db.session.commit()


def delete(event):
    db.session.delete(event)
    db.session.commit()


def delete_many(events):
    for e in events:
        db.session.delete(e)
    db.session.commit()
