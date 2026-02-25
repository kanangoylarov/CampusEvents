from datetime import datetime

from app.extensions import db


def cleanup_expired_events():
    """
    Delete events whose time slot has fully passed.

    An event is considered expired when:
      - Its date is before today, OR
      - Its date is today AND its end_time is set AND end_time < current time.

    Expired events are removed so their rooms become available again.
    """
    now = datetime.now()
    today = now.date()
    current_time = now.time()

    from app.models.event_model import Event

    expired = Event.query.filter(
        db.or_(
            # Past date
            Event.date < today,
            # Today but end_time already passed
            db.and_(
                Event.date == today,
                Event.end_time.isnot(None),
                Event.end_time < current_time,
            )
        )
    ).all()

    if expired:
        try:
            for event in expired:
                db.session.delete(event)
            db.session.commit()
        except Exception:
            db.session.rollback()
