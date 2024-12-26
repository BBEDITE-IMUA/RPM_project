import time
from functools import wraps
from typing import Any, Callable, Coroutine

from prometheus_client import Counter, Histogram

BUCKETS = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0,
    1.2,
    1.4,
    1.6,
    1.8,
    2.0,
    float('+inf'),
]

LATENCY = Histogram('latency_seconds_handler', 'Время задержку', labelnames=['handler'], buckets=BUCKETS)



def track_latency(
    method_name: str,
) -> Callable[[Callable[..., Coroutine[Any, Any, Any]]], Callable[..., Coroutine[Any, Any, Any]]]:
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> Callable[..., Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.monotonic()
            try:
                return await func(*args, **kwargs)
            finally:
                elapsed_time = time.monotonic() - start_time
                LATENCY.labels(handler=method_name).observe(elapsed_time)

        return wrapper

    return decorator


SEND_MESSAGE = Counter(
    'bot_messages_sent',
    'Отправленные сообщения в очередь',
)