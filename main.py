import asyncio
from link_search import LinkChecker

async def main():
    checker = LinkChecker()
    await checker.main()

if __name__ == "__main__":
    asyncio.run(main())
