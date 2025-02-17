import asyncio
from collections import defaultdict

import aiofiles
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook

from utils import start_animate_search

class LinkChecker:
    def __init__(self, max_depth=1, delay=1):
        self.visited_links = set()
        self.broken_links = []
        self.working_links = []
        self.link_paths = defaultdict(list)
        self.max_depth = max_depth
        self.delay = delay

    async def set_logs(self, error: str) -> None:
        """
        Записывает информацию об ошибках в файл error_logs.txt.

        Параметры:
            error (str): Текст ошибки.
        """
        async with aiofiles.open('error_logs.txt', 'a', encoding='utf-8') as f:
            await f.write(f"{error}\n")
            
    async def check_link(self, session, url, base_url):
        try:
            if url in self.visited_links:
                return
            self.visited_links.add(url)

            try:
                async with session.get(url) as response:
                    if response.status >= 400:
                        self.broken_links.append((url, response.status))
                    else:
                        self.working_links.append(url)
                        self.link_paths[url].append(base_url)
            except aiohttp.ClientError as e:
                self.broken_links.append((url, str(e)))

            await asyncio.sleep(self.delay)  # Задержка между запросами
        except Exception as e:  # pylint: disable=broad-exception-caught
            text_error = f"Ошибка в функции check_link - {e}"
            await self.set_logs(text_error)


    async def process_page(self, session, browser, url, depth):
        try:
            if depth > self.max_depth:
                return

            browser.get(url)
            await asyncio.sleep(2)  # Пауза для загрузки страницы

            links = browser.find_elements(By.TAG_NAME, 'a')
            tasks = []
            for link in links:
                href = link.get_attribute('href')
                if href and href.startswith('http'):
                    tasks.append(self.check_link(session, href, url))

            await asyncio.gather(*tasks)

            for link in self.working_links:
                await self.process_page(session, browser, link, depth + 1)
        except Exception as e:  # pylint: disable=broad-exception-caught
            text_error = f"Ошибка в функции process_page - {e}"
            await self.set_logs(text_error)

    async def save_to_excel(self, browser):
        wb = Workbook()
        ws = wb.active
        ws.title = "Broken Links"
        ws.append(["N п/п", "Ссылка", "Текст", "Ошибка", "Путь"])
        for i, (link, error) in enumerate(self.broken_links, 1):
            try:
                text = browser.find_element(By.TAG_NAME, 'a').text
            except Exception as e:  # pylint: disable=broad-exception-caught
                text = "Текст не найден"
                text_error = f"Ошибка в функции save_to_excel - {e}"
                await self.set_logs(text_error)
            path = ' -> '.join(self.link_paths[link])
            ws.append([i, link, text, error, path])
        wb.save("broken_links.xlsx")

    async def start_cheks(self):
        start_url = input("Введите ссылку: ")

        async with aiohttp.ClientSession() as session:
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--headless=new')
            browser = webdriver.Chrome(options=options)
            try:
                await start_animate_search(True)
                await self.process_page(session, browser, start_url, 1)
                await self.save_to_excel(browser)
            except Exception as e:  # pylint: disable=broad-exception-caught
                text_error = f"Ошибка в функции start_cheks - {e}"
                await self.set_logs(text_error)
            finally:
                await start_animate_search(False)
                print("Данные сохранены.")
                print("Конец проверки.")
                browser.quit()
