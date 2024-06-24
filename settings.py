import os

from dotenv import load_dotenv
load_dotenv()

# Валидные данные:
valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

# Невалидные данные:
invalid_email = os.getenv('invalid_email')
invalid_password = os.getenv('invalid_password')

