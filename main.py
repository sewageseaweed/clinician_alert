import asyncio
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv
from polling_service.polling_service import poll_clinicians_sequentially

'''
TODO:
- If number of clinicians increase, we have to scale the wait time to not go over QPS limit (100), or we round robin
'''
        
        
async def main():
    limiter = AsyncLimiter(max_rate = 96, time_period = 1)
    await poll_clinicians_sequentially(limiter)
    

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
