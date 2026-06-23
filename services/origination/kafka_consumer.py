from aiokafka import AIOKafkaConsumer
import json

async def start_consumer():
    consumer = AIOKafkaConsumer(
        "loan.submitted",
        bootstrap_servers="localhost:9092",
        group_id="origination-group",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Recieved event: {message.value}")
            print(f"Loan {message.value['loan_id']} submitted for customer {message.value['customer_id']}")
    finally:
        await consumer.stop()