import os


class InstanceConfig:
    DATABASE_URL = os.getenv('DATABASE_URL', 'chat.db')
    DEBUG = os.getenv('DEBUG', 'true') == 'true'
