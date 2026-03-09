import asyncio
from typing import Dict, List, Callable, Awaitable, Optional
from aiogram.types import Message


class MediaGroupManager:
    """
    Менеджер для сбора сообщений из одной медиагруппы (альбома) и их обработки единым колбэком.
    """

    def __init__(self, callback: Callable[[List[Message]], Awaitable[None]], delay: float = 0.5):
        """
        :param callback: асинхронная функция, которая будет вызвана с полным списком сообщений альбома.
        :param delay: задержка в секундах для ожидания остальных сообщений группы.
        """
        self.callback = callback
        self.delay = delay
        self._buffer: Dict[str, List[Message]] = {}
        self._tasks: Dict[str, asyncio.Task] = {}

    async def handle_message(self, message: Message) -> None:
        """
        Обрабатывает входящее сообщение. Если оно входит в медиагруппу — добавляет в буфер
        и планирует обработку. Если не входит — ничего не делает (предполагается,
        что такие сообщения обрабатываются отдельно).
        """
        media_group_id = message.media_group_id
        if not media_group_id:
            return  # не медиагруппа, игнорируем (или можно передать дальше)

        # Добавляем сообщение в буфер
        if media_group_id not in self._buffer:
            self._buffer[media_group_id] = []
        self._buffer[media_group_id].append(message)

        # Отменяем предыдущую задачу для этого media_group_id, если она была
        if media_group_id in self._tasks:
            self._tasks[media_group_id].cancel()

        # Создаём новую задачу
        task = asyncio.create_task(self._process_group(media_group_id))
        self._tasks[media_group_id] = task

    async def _process_group(self, media_group_id: str) -> None:
        """Ожидает задержку, затем извлекает сообщения из буфера и вызывает callback."""
        try:
            await asyncio.sleep(self.delay)
            # Забираем сообщения из буфера
            messages = self._buffer.pop(media_group_id, [])
            if messages:
                await self.callback(messages)
        finally:
            # Удаляем задачу из словаря, даже если произошла ошибка
            self._tasks.pop(media_group_id, None)

    def cancel_all(self) -> None:
        """Отменяет все запланированные задачи (полезно при остановке бота)."""
        for task in self._tasks.values():
            task.cancel()
        self._tasks.clear()
        self._buffer.clear()
