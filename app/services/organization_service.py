from app.models.organization_model import Organization
from app.repositories import organization_repository
from app.utils import save_uploaded_image, delete_uploaded_image


def list_organizations():
    return organization_repository.get_all_ordered_by_name()


def get_organization(org_id):
    return organization_repository.get_by_id(org_id)


def create_organization(form_data, picture_file):
    name = (form_data.get('name') or '').strip()
    if not name:
        return None, 'Organization name is required.'
    saved_filename = save_uploaded_image(picture_file)
    org = Organization(
        name=name,
        description=form_data.get('description'),
        picture=saved_filename,
    )
    organization_repository.save(org)
    return org, None


def update_organization(org_id, form_data, picture_file):
    org = organization_repository.get_by_id(org_id)
    name = (form_data.get('name') or '').strip()
    if not name:
        return None, 'Organization name is required.'
    saved_filename = save_uploaded_image(picture_file)
    if saved_filename:
        delete_uploaded_image(org.picture)
        org.picture = saved_filename
    org.name = name
    org.description = form_data.get('description')
    organization_repository.update()
    return org, None


def delete_organization(org_id):
    org = organization_repository.get_by_id(org_id)
    delete_uploaded_image(org.picture)
    organization_repository.delete(org)
