from sqlalchemy.orm import Session
from app.models import Package
from app.schemas import PackageCreate
from typing import List, Optional

def get_package(db: Session, package_id: int):
    return db.query(Package).filter(Package.id == package_id).first()

def get_packages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Package).offset(skip).limit(limit).all()

def create_package(db: Session, package: PackageCreate, session_id: str):
    db_package = Package(
        name=package.name,
        weight=package.weight,
        content_cost=package.content_cost,
        package_type_id=package.package_type_id,
        session_id=session_id
    )
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

def get_packages_filtered(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    package_type_id: Optional[int] = None,
    has_delivery_cost: Optional[bool] = None,
    session_id: Optional[str] = None
) -> List[Package]:
    query = db.query(Package)

    if package_type_id is not None:
        query = query.filter(Package.package_type_id == package_type_id)

    if has_delivery_cost is not None:
        if has_delivery_cost:
            query = query.filter(Package.delivery_cost.isnot(None))
        else:
            query = query.filter(Package.delivery_cost.is_(None))

    if session_id is not None:
        query = query.filter(Package.session_id == session_id)

    return query.offset(skip).limit(limit).all()