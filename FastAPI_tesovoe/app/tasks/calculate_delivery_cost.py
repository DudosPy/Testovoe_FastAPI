import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Package
from app.utils.currency import get_usd_to_rub_rate
from app.mongodb import logs_collection
from datetime import datetime

logger = logging.getLogger(__name__)

def calculate_delivery_cost_for_package(db: Session, package: Package):
    try:
        usd_to_rub_rate = get_usd_to_rub_rate()
        delivery_cost = (package.weight * 0.5 + package.content_cost * 0.01) * usd_to_rub_rate
        package.delivery_cost = delivery_cost
        db.commit()
        db.refresh(package)
        logger.info(f"Calculated delivery cost for package {package.id}: {delivery_cost} RUB")
    except Exception as e:
        logger.error(f"Error calculating delivery cost for package {package.id}: {e}")
        # Логирование в MongoDB
        log_entry = {
            "package_id": package.id,
            "delivery_cost": delivery_cost,
            "calculated_at": datetime.utcnow()
        }
        logs_collection.insert_one(log_entry)

        logger.info(f"Calculated delivery cost for package {package.id}: {delivery_cost} RUB")
    except Exception as e:
        logger.error(f"Error calculating delivery cost for package {package.id}: {e}")

def calculate_delivery_costs():
    db = SessionLocal()
    try:
        packages = db.query(Package).filter(Package.delivery_cost.is_(None)).all()
        logger.info(f"Found {len(packages)} packages without delivery cost")
        for package in packages:
            calculate_delivery_cost_for_package(db, package)
    except Exception as e:
        logger.error(f"Error calculating delivery costs: {e}")
    finally:
        db.close()