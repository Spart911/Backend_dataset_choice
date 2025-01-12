import os
import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException, Form
from starlette.responses import FileResponse

app = FastAPI()

BASE_DIR = Path("data")
MAIN_FOLDER = BASE_DIR / "main"
TARGET_FOLDER = BASE_DIR / "targets"

# Убедимся, что все папки существуют
os.makedirs(MAIN_FOLDER, exist_ok=True)
os.makedirs(TARGET_FOLDER, exist_ok=True)

# Создание папок для чисел от 0 до 10
for i in range(11):
    os.makedirs(TARGET_FOLDER / str(i), exist_ok=True)

@app.get("/get-test")
async def get_test():
    """Эндпоинт для отправки тестового изображения."""
    files = list(MAIN_FOLDER.glob("*.*"))
    if not files:
        raise HTTPException(status_code=404, detail="No files in the main folder.")

    photo = files[0]
    return {"uid": photo.name, "photo_url": f"/photo/{photo.name}"}

@app.get("/photo/{uid}")
async def serve_photo(uid: str):
    """Эндпоинт для получения фото по UID."""
    file_path = MAIN_FOLDER / uid
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Photo not found.")
    return FileResponse(file_path)

@app.post("/process-test")
async def process_test(uid: str = Form(...), target: str = Form(...)):
    """
    Эндпоинт для обработки теста.
    Принимает UID и список чисел. Раскладывает фото по папкам и удаляет из основной папки.
    """
    # Преобразуем target в список чисел
    target_numbers = [int(t) for t in target.split(",")]

    # Проверка чисел
    if any(t < 0 or t > 10 for t in target_numbers):
        raise HTTPException(status_code=400, detail="Target numbers must be between 0 and 10.")

    file_path = MAIN_FOLDER / uid
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Photo not found in the main folder.")

    # Раскладываем фото по папкам
    for t in target_numbers:
        target_folder = TARGET_FOLDER / str(t)
        shutil.copy(file_path, target_folder / uid)

    # Удаляем фото из основной папки
    file_path.unlink()

    return {"status": "success", "uid": uid, "distributed_to": target_numbers}
