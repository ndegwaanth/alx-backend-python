import asyncio
import aiohttp


async def show_generator():
    for i in range(10):
        await asyncio.sleep(1) #simulate
        yield i


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def async_data_generator(urls):
    for url in urls:
        data = await fetch_data(url)
        yield data

async def main():
    async for value in show_generator():
        print(value)

    urls = [
        'https://www.google.com',
        'https://www.youtube.com'
    ]

    async for data in async_data_generator(urls):
        print(data)

asyncio.run(main())