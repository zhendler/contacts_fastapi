import cloudinary
from dotenv import dotenv_values

dotenv_values()
def configure_cloudinary():
    cloudinary.config(
        cloud_name="dh6k5dykl",
        api_key="766446158224791",
        api_secret="RhTF7ZVi6wKWnNOuu2MmFMxD5Os"
    )
