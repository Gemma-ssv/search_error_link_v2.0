import asyncio
from link_search import LinkChecker

async def main():
    checker = LinkChecker()
    await checker.start_cheks()

if __name__ == "__main__":
    asyncio.run(main())
