import shutil

from fastapi import APIRouter, UploadFile

from src.core.tasks.tasks import resize_and_save_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("")
def upload_image(
        file: UploadFile
):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    resize_and_save_image.delay(image_path)

    return {
        "filename": file.filename
    }