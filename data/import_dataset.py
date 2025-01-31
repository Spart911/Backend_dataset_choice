import os
import shutil
import os
from pathlib import Path

def copy_and_number_photos(source_dirs, target_dir):
    """
    Копирует все фотографии из указанных папок в одну папку target_dir
    и нумерует их в порядке возрастания, начиная с 0.

    :param source_dirs: Список путей к папкам с фотографиями
    :param target_dir: Путь к папке, куда будут скопированы фотографии
    """
    # Создать папку назначения, если она не существует
    os.makedirs(target_dir, exist_ok=True)

    # Поддерживаемый список расширений изображений
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

    # Счётчик для именования фотографий
    counter = 0

    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if not source_path.exists() or not source_path.is_dir():
            print(f"Пропуск: Папка '{source_dir}' не существует или не является папкой.")
            continue

        for file in source_path.iterdir():
            if file.suffix.lower() in image_extensions:
                # Генерируем новое имя для фото
                new_name = f"{counter}{file.suffix.lower()}"
                target_path = Path(target_dir) / new_name

                # Копируем файл
                shutil.copy(file, target_path)
                counter += 1

    print(f"Готово! Скопировано {counter} фотографий в папку '{target_dir}'.")

# Пример использования
if __name__ == "__main__":
    # Укажите пути к исходным папкам с фотографиями
    source_folders = [
        r"C:\Users\egor2\PycharmProjects\AI-CLOTH\my_dataset_500\blobs_500",
        r"C:\Users\egor2\PycharmProjects\AI-CLOTH\my_dataset_500\great_500",
        r"C:\Users\egor2\PycharmProjects\AI-CLOTH\my_dataset_500\rassloienie_500",
        r"C:\Users\egor2\PycharmProjects\AI-CLOTH\my_dataset_500\re-extrusion_500",
        r"C:\Users\egor2\PycharmProjects\AI-CLOTH\my_dataset_500\ringing_500",
        r"C:\Users\egor2\PycharmProjects\AI-CLOTH\my_dataset_500\stringing_500",
        r"C:\Users\egor2\PycharmProjects\AI-CLOTH\my_dataset_500\underextrusion_500",
        r"C:\Users\egor2\PycharmProjects\AI-CLOTH\my_dataset_500\warping_500",
    ]

    # Укажите путь к целевой папке
    main_folder = "main"

    copy_and_number_photos(source_folders, main_folder)
