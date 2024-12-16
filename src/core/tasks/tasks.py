import asyncio

from pydantic import EmailStr

from src.core.tasks.celery_app import celery_instance

from PIL import Image
import os

from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBManager

WIDTHS = [1000, 500, 200]


@celery_instance.task
def resize_and_save_image(input_path, output_dir="src/static/images"):
    """
    Resizes an input image to specified widths and saves them to a directory.

    Parameters:
        input_path (str): Path to the input image.
        output_dir (str): Directory to save resized images. Defaults to "src/static/images".
    """
    try:
        # Open the input image
        with Image.open(input_path) as img:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Loop through the specified widths
            for width in WIDTHS:
                # Calculate new height preserving the aspect ratio
                aspect_ratio = img.height / img.width
                height = int(width * aspect_ratio)

                # Resize the image
                resized_img = img.resize((width, height), Image.LANCZOS)  # type: ignore

                # Create a new filename
                base_name = os.path.basename(input_path)
                name, ext = os.path.splitext(base_name)
                new_file_name = f"{name}_{width}px{ext}"

                # Save the resized image
                output_path = os.path.join(output_dir, new_file_name)
                resized_img.save(output_path)

                print(f"Saved resized image: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


async def get_booking_with_today_checkin_helper():
    print("task started")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(bookings)


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_booking_with_today_checkin_helper())


@celery_instance.task()
def send_email_notification_on_booking_creation(email: EmailStr):
    with open("log.txt", "a") as log:
        log.write(f"email sent to {email}")
