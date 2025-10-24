#!/usr/bin/python3.10

import sys
import os

# Добавляем путь к проекту в PYTHONPATH
path = '/home/yourusername/mysite'  # Замените yourusername на ваше имя пользователя
if path not in sys.path:
    sys.path.append(path)

# Устанавливаем переменную окружения для конфигурации
os.environ['FLASK_ENV'] = 'production'

from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
