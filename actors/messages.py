from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from enum import Enum


# Базовые типы сообщений
class MessageType(str, Enum):
    """Типы сообщений в системе акторов"""
    PING = 'ping'
    PONG = 'pong'
    ERROR = 'error'
    SHUTDOWN = 'shutdown'
    DLQ_QUEUED = 'dlq_queued'
    DLQ_PROCESSED = 'dlq_processed'
    DLQ_CLEANUP = 'dlq_cleanup'


# Для обратной совместимости
MESSAGE_TYPES = {
    'PING': MessageType.PING,
    'PONG': MessageType.PONG,
    'ERROR': MessageType.ERROR,
    'SHUTDOWN': MessageType.SHUTDOWN,
    'DLQ_QUEUED': MessageType.DLQ_QUEUED,
    'DLQ_PROCESSED': MessageType.DLQ_PROCESSED,
    'DLQ_CLEANUP': MessageType.DLQ_CLEANUP
}


@dataclass
class ActorMessage:
    """Базовый класс для всех сообщений между акторами"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: Optional[str] = None
    message_type: str = ''
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, 
               sender_id: Optional[str] = None,
               message_type: str = '',
               payload: Optional[Dict[str, Any]] = None) -> 'ActorMessage':
        """Фабричный метод для удобного создания сообщений"""
        return cls(
            sender_id=sender_id,
            message_type=message_type,
            payload=payload or {}
        )