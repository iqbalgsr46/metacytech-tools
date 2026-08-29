import asyncio
from typing import List, Callable, Any

async def run_parallel(tasks: List[Callable], max_concurrent: int = 5) -> List[Any]:
    sem = asyncio.Semaphore(max_concurrent)
    
    async def worker(task):
        async with sem:
            if asyncio.iscoroutinefunction(task):
                return await task()
            result = task()
            if asyncio.iscoroutine(result):
                return await result
            return result
    
    return await asyncio.gather(*(worker(t) for t in tasks), return_exceptions=True)
