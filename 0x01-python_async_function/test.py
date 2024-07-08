import asyncio
import string
import random


async def hello_world():
    print("Helo")
    await asyncio.sleep(1)
    print("World")

async def main():
    await hello_world()


asyncio.run(main())


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=length))
    return password

print(generate_password(10))