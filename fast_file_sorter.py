import os
import argparse
import shutil
from pathlib import Path
import threading
import logging

# Налаштування логування для виводу інформаційних повідомлень
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Функція, яка отримує список файлів за розширеннями у вказаній папці
def get_files_by_extension(folder_path):
    files_by_extension = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file)
            if extension not in files_by_extension:
                files_by_extension[extension] = []
            files_by_extension[extension].append(file_path)
    return files_by_extension

# Функція, яка копіює файли до відповідних папок за розширенням
def copy_files(files_by_extension, destination_folder):
    for extension, files in files_by_extension.items():
        extension_folder = os.path.join(destination_folder, extension[1:].upper())  # Створюємо шлях до папки з розширенням у великих літерах
        os.makedirs(extension_folder, exist_ok=True)  # Створюємо папку, якщо вона не існує
        for file_path in files:
            shutil.copy(file_path, extension_folder)  # Копіюємо файл до відповідної папки

# Функція для обробки папки з використанням паралельного виконання у кількох потоках
def process_folder(source_folder, destination_folder, num_threads):
    files_by_extension = get_files_by_extension(source_folder)  # Отримуємо список файлів за розширеннями у вихідній папці
    threads = []  # Створюємо список для зберігання об'єктів потоків
    for _ in range(num_threads):
        thread = threading.Thread(target=copy_files, args=(files_by_extension, destination_folder))  # Створюємо потік
        thread.start()  # Запускаємо потік
        threads.append(thread)  # Додаємо потік до списку
    for thread in threads:
        thread.join()  # Чекаємо завершення роботи всіх потоків

# Головна функція для обробки аргументів командного рядка та запуску обробки папки
def main():
    parser = argparse.ArgumentParser(description='Sort files by extension in a folder using multiple threads.')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')  # Аргумент для вказання вихідної папки
    parser.add_argument('--num_threads', type=int, default=4, help='Number of threads for parallel processing')  # Опціональний аргумент для вказання кількості потоків
    args = parser.parse_args()

    source_folder = args.source_folder  # Отримуємо шлях до вихідної папки з аргументів командного рядка
    num_threads = args.num_threads  # Отримуємо кількість потоків з аргументів командного рядка

    destination_folder = os.path.join(os.path.dirname(source_folder), 'Sort_files')  # Формуємо шлях до папки "Сортовані_файли" в тій же папці, що і вихідна
    logging.info(f'Starting processing of folder {source_folder} with {num_threads} threads...')  # Логуємо інформацію про початок обробки папки
    process_folder(source_folder, destination_folder, num_threads)  # Запускаємо обробку папки
    logging.info('Processing completed.')  # Логуємо інформацію про завершення обробки папки

if __name__ == "__main__":
    main()
