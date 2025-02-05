from sqlalchemy.orm import Session
from app.models import PackageType
from app.schemas import PackageTypeCreate

def get_package_type(db: Session, package_type_id: int):
    return db.query(PackageType).filter(PackageType.id == package_type_id).first()

def get_package_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PackageType).offset(skip).limit(limit).all()

def create_package_type(db: Session, package_type: PackageTypeCreate):
    db_package_type = PackageType(name=package_type.name)
    db.add(db_package_type)
    db.commit()
    db.refresh(db_package_type)
    return db_package_type