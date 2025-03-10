import time
import asyncio
from telogger import Telogger, monitor

class DataProcessor:
    def __init__(self):
        self.telogger = Telogger()  # Using environment variables
    
    @monitor(name="Complex Calculation")
    def calculate(self):
        time.sleep(2)
        return 42
    
    @monitor(name="Async Fetch")
    async def fetch_data(self):
        await asyncio.sleep(1)
        return {"status": "success"}

def main():
    processor = DataProcessor()
    print("Result:", processor.calculate())
    asyncio.run(processor.fetch_data())

if __name__ == "__main__":
    main()