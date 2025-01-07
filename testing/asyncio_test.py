import asyncio
from speed_test import speed_test

async def get_data(id: int, delay: float):
    print(f'Coroutine {id} started')
    await asyncio.sleep(delay)
    return {'id': id, 'data': 'Some cool data here'}

async def set_future_result(future, value):
    await asyncio.sleep(2)
    future.set_result(value)
    print(f"Set the future's result to: {value}")

async def main():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    
    asyncio.create_task(set_future_result(future, 'Future result is ready'))
    
    result = await future
    print(f"Received the future's result: {result}")

@speed_test
def RunTasks():
    print('Running tasks')
    asyncio.run(main())

RunTasks()