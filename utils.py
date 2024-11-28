
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

def print_choice(urls: set) -> set:
    """
    Выводит информацию о программе. Запрашивает у пользователя ссылки.

    Аргументы:
        urls (set): Получает пустой список, в который будут записаны ссылки.

    Возвращает:
        set: Возвращает список ссылок, которые ввёл пользователь.
    """
    example_text = (
        "Программа предназначена для проверки ссылок в новостях в интернет-магазине.\n"
        "Введите ссылку в формате - https://домен/путь/\n"
        "Например - https://gemma.by/news/\n"
        "После ввода нажмите - Enter.\n"
    )
    print_slowly(example_text)
    
    while True:
        example_text = "Введите ссылку: "
        print_slowly(example_text)
        url_input = input().strip()

        if is_valid_url(url_input):
            urls.add(url_input)
            while True:
                choice_text = ("Выполнить поиск? Введите `да` или `нет`.\n"
                               "Если `нет`, то можно будет добавить еще ссылку.\n")
                print_slowly(choice_text)
                next_input = input().lower().strip()

                if next_input == 'да':
                    answer_yes_text = "Дождитесь окончания выполнения программы.\n"
                    print_slowly(answer_yes_text)
                    return urls
                elif next_input == 'нет':
                    break
                else:
                    wrong_answer_text = "Неправильный ответ. Требуется ввести `да` или `нет`.\n"
                    print_slowly(wrong_answer_text)
                    continue
        else:
            wrong_link_text = "Вы ввели неправильный формат ссылки. Попробуйте еще раз.\n"
            print_slowly(wrong_link_text)
            continue