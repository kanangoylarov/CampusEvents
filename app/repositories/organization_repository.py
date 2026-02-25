from app.extensions import db
from app.models.organization_model import Organization


def get_all_ordered_by_name():
    return Organization.query.order_by(Organization.name).all()


def get_by_id(org_id):
    return db.get_or_404(Organization, org_id)


def save(org):
    db.session.add(org)
    db.session.commit()


def update():
    db.session.commit()


def delete(org):
    db.session.delete(org)
    db.session.commit()
