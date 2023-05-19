import cloudinary
import cloudinary.uploader
from app.config import settings


cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.api_key,
    api_secret=settings.api_secret,
)

# uncompleted
def save_file_to_cloudinary(file_data):
    try:
        upload_result = cloudinary.uploader.upload(file_data)
        # insert file url into the file table and log to the logging service
        print(upload_result["url"])
    except Exception as e:
        print(e)
        return None
