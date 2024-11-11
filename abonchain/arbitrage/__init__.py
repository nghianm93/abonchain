# abonchain/__init__.py

# Làm cho Celery được khởi chạy cùng lúc với Django
from .celery import app as celery_app

__all__ = ("celery_app",)
