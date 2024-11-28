
import time
import threading
import re
import openpyxl


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
    with console_lock:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
