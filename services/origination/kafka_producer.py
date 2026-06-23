from aiokafka import AIOKafkaProducer
import json

producer = None

async def start_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    await producer.start()

async def stop_producer():
    global producer
    if producer:
        await producer.stop()

async def publish_event(topic: str, event: dict):
    global producer
    await producer.send_and_wait(topic, event)