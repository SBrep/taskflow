import random
import time


def unstable_service() -> str:
    """Имитация нестабильного внешнего сервиса"""
    time.sleep(0.05)
    if random.random() < 0.5:          # 50% шанс ошибки
        raise Exception("External API temporary failure")
    return "External service OK"