from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

try:
    from ..storage import EVENT_LOG
except ImportError:
    from storage import EVENT_LOG


EventHandler = Callable[[dict], None]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        handlers = self._subscribers.setdefault(event_type, [])
        if handler not in handlers:
            handlers.append(handler)

    def publish(self, event_type: str, data: dict) -> None:
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        EVENT_LOG.append(event)
        for handler in self._subscribers.get(event_type, []):
            handler(event)
        for handler in self._subscribers.get("*", []):
            handler(event)


EVENT_BUS = EventBus()
