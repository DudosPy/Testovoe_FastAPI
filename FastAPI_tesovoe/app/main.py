import json
import logging
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db
from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks.calculate_delivery_cost import calculate_delivery_costs
from app.rabbitmq import send_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

scheduler = BackgroundScheduler()
scheduler.add_job(calculate_delivery_costs, 'interval', minutes=5)
scheduler.start()
logger.info("Scheduler started")

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    logger.info("Scheduler stopped")

@app.get("/")
def read_root():
    return {"message": "Delivery Service is running!"}

# Роут для получения списка типов посылок
@app.get("/package-types/", response_model=list[schemas.PackageType], summary="Получить список типов посылок")
def read_package_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    package_types = crud.get_package_types(db, skip=skip, limit=limit)
    return package_types

# Роут для создания типа посылки
@app.post("/package-types/", response_model=schemas.PackageType, summary="Добавить новый тип посылки")
def create_package_type(package_type: schemas.PackageTypeCreate, db: Session = Depends(get_db)):
    return crud.create_package_type(db=db, package_type=package_type)

# Роут для получения списка посылок
@app.get("/packages/", response_model=list[schemas.Package], summary="Получить список посылок")
def read_packages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    packages = crud.get_packages(db, skip=skip, limit=limit)
    return packages

# Роут для создания посылки
@app.post("/packages/", response_model=schemas.Package, summary="Создать посылку")
def create_package(package: schemas.PackageCreate, db: Session = Depends(get_db)):
    session_id = "example_session_id"
    db_package = crud.create_package(db=db, package=package, session_id=session_id)
    send_message("package_queue", json.dumps({"id": db_package.id}))
    logger.info(f'Created package with ID {db_package.id}')
    return db_package

@app.get("/packages/{package_id}", response_model=schemas.Package, summary="Получить послылку по id")
def read_package(package_id: int, db: Session = Depends(get_db)):
    db_package = crud.get_package(db, package_id=package_id)
    if db_package is None:
        logger.error(f"Package with ID {package_id} not found")
        raise HTTPException(status_code=404, detail="Package not found")
    return db_package

@app.get("/user/packages/", response_model=list[schemas.Package], summary="Получить список посылок пользователя")
def read_user_packages(
    skip: int = 0,
    limit: int = 100,
    package_type_id: Optional[int] = None,
    has_delivery_cost: Optional[bool] = None,
    db: Session = Depends(get_db)
    ):
    session_id = "example_session_id"
    packages = crud.get_packages_filtered(
        db,
        skip=skip,
        limit=limit,
        package_type_id=package_type_id,
        has_delivery_cost=has_delivery_cost,
        session_id=session_id
    )
    return packages

@app.post("/tasks/calculate-delivery-costs/", summary="Рассчитать стоимость доставки")
def trigger_calculate_delivery_costs():
    calculate_delivery_costs()
    return {"message": "Delivery costs calculation started"}