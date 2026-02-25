import os
import uuid
from datetime import datetime

from werkzeug.utils import secure_filename

from app.extensions import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(file):
    """Save an uploaded image file and return the stored filename, or None."""
    if file and file.filename and allowed_file(file.filename):
        ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        file.save(os.path.join(UPLOAD_FOLDER, unique_name))
        return unique_name
    return None


def delete_uploaded_image(filename):
    """Delete an uploaded image file if it exists."""
    if filename:
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(path):
            os.remove(path)


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
