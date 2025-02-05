import pika
from app.database import SessionLocal
from app.models import Package
from app.utils.currency import get_usd_to_rub_rate
import json

def process_message(ch, method, properties, body):
    db = SessionLocal()
    try:
        package_data = json.loads(body)
        package = db.query(Package).filter(Package.id == package_data["id"]).first()
        if package:
            usd_to_rub_rate = get_usd_to_rub_rate()
            delivery_cost = (package.weight * 0.5 + package.content_cost * 0.01) * usd_to_rub_rate
            package.delivery_cost = delivery_cost
            db.commit()
            db.refresh(package)
    finally:
        db.close()

def start_worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()
    channel.queue_declare(queue="package_queue")
    channel.basic_consume(queue="package_queue", on_message_callback=process_message, auto_ack=True)
    channel.start_consuming()