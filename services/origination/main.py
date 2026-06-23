from fastapi import FastAPI
from routes import router
from kafka_producer import start_producer, stop_producer
from kafka_consumer import start_consumer
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        await start_producer()
        print("Kafka producer started")
    except Exception as e:
        print(f"Failed to start producer: {e}")
    asyncio.create_task(start_consumer())
    yield
    await stop_producer()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/health")
def health():
    return { "status": "ok" }