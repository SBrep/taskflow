import threading

is_shutting_down: bool = False
active_requests: int = 0
total_requests: int = 0          # Новый счётчик для ЛР 5

# Блокировка для защиты общего состояния
lock = threading.Lock()