from app.models.room_model import Room
from app.repositories import room_repository
from app.services import event_service
from app.utils import save_uploaded_image, delete_uploaded_image


def list_rooms():
    event_service.cleanup_expired_events()
    return room_repository.get_all_ordered_by_name()


def get_room(room_id):
    return room_repository.get_by_id(room_id)


def create_room(form_data, picture_file):
    saved_filename = save_uploaded_image(picture_file)
    room = Room(
        room_name=form_data.get('room_name'),
        picture=saved_filename,
        capacity=form_data.get('capacity') or None,
        location=form_data.get('location'),
    )
    room_repository.save(room)
    return room


def update_room(room_id, form_data, picture_file):
    room = room_repository.get_by_id(room_id)
    saved_filename = save_uploaded_image(picture_file)
    if saved_filename:
        delete_uploaded_image(room.picture)
        room.picture = saved_filename
    room.room_name = form_data.get('room_name')
    room.location = form_data.get('location')
    room.capacity = form_data.get('capacity') or None
    room_repository.update()
    return room


def delete_room(room_id):
    room = room_repository.get_by_id(room_id)
    delete_uploaded_image(room.picture)
    room_repository.delete(room)
