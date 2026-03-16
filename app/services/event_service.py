from datetime import date, time, datetime

from app.models.event_model import Event
from app.repositories import event_repository, room_repository
from app.utils import save_uploaded_image, delete_uploaded_image


def parse_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def parse_time(value):
    if not value:
        return None
    try:
        parts = value.split(':')
        return time(int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return None


def check_room_conflict(room_id, event_date, new_start, new_end, exclude_id=None):
    if not room_id or not event_date:
        return False, None

    existing_events = event_repository.find_by_room_and_date(
        room_id, event_date, exclude_id
    )
    for existing in existing_events:
        if existing.start_time is None or new_start is None:
            return True, existing

        existing_end = existing.end_time if existing.end_time else time(23, 59)
        new_end_safe = new_end if new_end else time(23, 59)

        if new_start < existing_end and existing.start_time < new_end_safe:
            return True, existing

    return False, None


def format_conflict_message(room_id, event_date, blocking):
    room = room_repository.get_by_id(int(room_id))
    start_str = blocking.start_time.strftime('%H:%M') if blocking.start_time else '?'
    end_str = blocking.end_time.strftime('%H:%M') if blocking.end_time else 'end of day'
    return (
        f'Room "{room.room_name}" is already booked on {event_date} '
        f'({start_str} \u2013 {end_str}) by "{blocking.name}". '
        f'Choose a different room or a non-overlapping time slot.'
    )


def list_events(filters):
    cleanup_expired_events()
    org_id = filters.get('org_id', '').strip() or None
    date_from = parse_date(filters.get('date_from', '').strip())
    date_to = parse_date(filters.get('date_to', '').strip())
    time_from = parse_time(filters.get('time_from', '').strip())
    time_to = parse_time(filters.get('time_to', '').strip())
    return event_repository.filter_events(org_id, date_from, date_to, time_from, time_to)


def create_event(form_data, picture_file):
    room_id = form_data.get('room_id') or None
    event_date = parse_date(form_data.get('date'))
    start_time = parse_time(form_data.get('start_time'))
    end_time = parse_time(form_data.get('end_time'))

    name = (form_data.get('name') or '').strip()
    if not name:
        return None, 'Event name is required.'
    if not event_date:
        return None, 'Event date is required.'

    if room_id and event_date:
        conflict, blocking = check_room_conflict(room_id, event_date, start_time, end_time)
        if conflict:
            return None, format_conflict_message(room_id, event_date, blocking)

    saved_filename = save_uploaded_image(picture_file)
    event = Event(
        name=name,
        description=form_data.get('description'),
        picture=saved_filename,
        private=bool(form_data.get('private')),
        date=event_date,
        for_registration=form_data.get('for_registration'),
        start_time=start_time,
        end_time=end_time,
        room_id=room_id,
        capacity=form_data.get('capacity') or None,
        organization_id=form_data.get('organization_id') or None,
    )
    event_repository.save(event)
    return event, None


def update_event(event_id, form_data, picture_file):
    event = event_repository.get_by_id(event_id)
    room_id = form_data.get('room_id') or None
    event_date = parse_date(form_data.get('date'))
    start_time = parse_time(form_data.get('start_time'))
    end_time = parse_time(form_data.get('end_time'))

    if room_id and event_date:
        conflict, blocking = check_room_conflict(
            room_id, event_date, start_time, end_time, exclude_id=event.id
        )
        if conflict:
            return event, format_conflict_message(room_id, event_date, blocking)

    saved_filename = save_uploaded_image(picture_file)
    if saved_filename:
        delete_uploaded_image(event.picture)
        event.picture = saved_filename

    event.name = (form_data.get('name') or '').strip() or event.name
    event.description = form_data.get('description')
    event.private = bool(form_data.get('private'))
    event.date = event_date
    event.for_registration = form_data.get('for_registration')
    event.start_time = start_time
    event.end_time = end_time
    event.room_id = room_id
    event.capacity = form_data.get('capacity') or None
    event.organization_id = form_data.get('organization_id') or None

    event_repository.update()
    return event, None


def delete_event(event_id):
    event = event_repository.get_by_id(event_id)
    delete_uploaded_image(event.picture)
    event_repository.delete(event)


def cleanup_expired_events():
    now = datetime.now()
    expired = event_repository.find_expired(now.date(), now.time())
    if expired:
        try:
            event_repository.delete_many(expired)
        except Exception:
            from app.extensions import db
            db.session.rollback()
