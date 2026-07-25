import asyncio 
from app.database import Base, engine 
from app.models import DetectedObject, DetectionTask

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    print("✅Tables a successfully created")
    
if __name__ == "__main__":
    asyncio.run(init_models())