import aiohttp
import asyncio

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://192.168.50.162:3000/queue') as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Error: {response.status}")
                return None  # or any default value you want to assign in case of an error
def getData():
    data = asyncio.run(fetch_data())
    return data