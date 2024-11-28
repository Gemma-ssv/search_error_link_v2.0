
import asyncio
import threading
import re


# Добавляем блокировку для синхронизации вывода в консоль
console_lock = threading.Lock()

def print_slowly(text, delay=0.05):
    """
    Выводит текст на экран посимвольно с заданной задержкой между символами.

    Эта функция используется для создания эффекта "медленного" вывода текста,
    что может быть полезно для драматического эффекта или для улучшения читаемости
    длинных текстов.

    Аргументы:
        text (str): Текст, который нужно вывести на экран.
        delay (float, optional): Задержка между выводом каждого символа в секундах.
            По умолчанию 0.05 секунды.

    Возвращает:
        None: Функция ничего не возвращает, она только выводит текст на экран.

    Пример:
        >>> print_slowly("Привет, мир!", delay=0.1)
        Привет, мир!
    """
    for char in text:
        print(char, end='', flush=True)
        asyncio.sleep(delay)
    print()

def clean_filename(url):
    """
    Очищает URL-адрес от недопустимых символов для использования в именах файлов.

    Аргументы:
        url (str): URL-адрес для очистки.

    Возвращает:
        str: Очищенный URL-адрес.
    """
    # Удаляем все символы, которые не являются буквами, цифрами или подчеркиванием
    cleaned_url = re.sub(r'[^a-zA-Z0-9_]', '_', url)
    return cleaned_url

def is_valid_url(url_input):
    """
    Проверяет валидность ссылки. 
    Аргументы:
        url_input (str): Ссылка, которую пользователь ввел через консоль.

    Возвращает:
        bool: Правильный формат или неправильный формат ссылки.
    """
    pass

async def animate_search(stop_event):
    """
    Анимирует процесс поиска, отображая вращающийся символ.

    Эта функция создает анимацию, которая имитирует процесс поиска.
    Она отображает вращающийся символ ("|", "/", "-", "\\") каждые полсекунды,
    пока не будет установлен `stop_event`.

    Аргументы:
        stop_event (asyncio.Event): Событие для остановки анимации.

    Возвращает:
        None: Функция ничего не возвращает, она только отображает анимацию.
    """
    symbols = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        print(f"\rВеду поиск - {symbols[i]}", end='', flush=True)
        await asyncio.sleep(0.5)
        i = (i + 1) % len(symbols)
    # Очистка строки после завершения анимации
    print("\rВеду поиск - ", end='', flush=True)

async def test(flag):    
    stop_event = asyncio.Event()
    # Запуск анимации в отдельном таске
    animation_task = asyncio.create_task(animate_search(stop_event))
    
    if flag == False:
        # Остановка анимации
        stop_event.set()
        # Ожидание завершения задачи анимации
        await animation_task

# Пример использования
async def main():
    await test(True)  # Запуск анимации
    await asyncio.sleep(5)  # Имитация работы
    await test(False)  # Остановка анимации

# Запуск асинхронной функции main
asyncio.run(main())