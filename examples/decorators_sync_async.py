import time
import asyncio
from telogger import Telogger, monitor, monitor_start_stop

tlogger = Telogger()

@monitor(telogger=tlogger, name="File Processor")
def process_file():
    time.sleep(1.5)
    print("File processed")

@monitor_start_stop(telogger=tlogger, name="Async Analyzer")
async def analyze_data():
    await asyncio.sleep(1)
    print("Data analyzed")

def main():
    process_file()
    asyncio.run(analyze_data())

if __name__ == "__main__":
    main()