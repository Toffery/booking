import time

from src.core.tasks.celery_app import celery_instance


@celery_instance.task
def test():
    time.sleep(5)
    print("task executed")

