import threading

is_shutting_down: bool = False
active_requests: int = 0
total_requests: int = 0

# Метрики для ЛР 6
total_errors: int = 0
total_tasks_created: int = 0

lock = threading.Lock()