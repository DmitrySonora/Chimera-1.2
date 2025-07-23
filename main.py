import asyncio
from config.logging import setup_logging
from actors.actor_system import ActorSystem
from actors.messages import ActorMessage, MESSAGE_TYPES
from tests.fixtures import EchoActor


async def main():
    """Демонстрация работы Actor System"""
    # Настраиваем логирование
    setup_logging()
    
    # Создаем систему акторов
    system = ActorSystem("demo")
    
    # Создаем и регистрируем акторы
    echo1 = EchoActor("echo-1", "Echo1")
    echo2 = EchoActor("echo-2", "Echo2")
    
    await system.register_actor(echo1)
    await system.register_actor(echo2)
    
    # Запускаем систему
    await system.start()
    
    print("=== Actor System запущена ===")
    print("Отправляем PING сообщения...")
    
    # Отправляем несколько сообщений
    for i in range(5):
        msg = ActorMessage.create(
            sender_id="main",
            message_type=MESSAGE_TYPES['PING'],
            payload={'count': i}
        )
        await system.send_message("echo-1", msg)
        
    # Broadcast сообщение
    broadcast_msg = ActorMessage.create(
        sender_id="main",
        message_type=MESSAGE_TYPES['PING'],
        payload={'broadcast': True}
    )
    await system.broadcast_message(broadcast_msg)
    
    # Даем время на обработку
    await asyncio.sleep(1)
    
    print(f"\nEcho1 обработал {echo1.processed_count} сообщений")
    print(f"Echo2 обработал {echo2.processed_count} сообщений")
    
    # Останавливаем систему
    print("\n=== Останавливаем систему ===")
    await system.stop()
    
    print("Готово!")


if __name__ == "__main__":
    asyncio.run(main())