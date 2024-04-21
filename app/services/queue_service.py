import json

import aio_pika


class RbQueueService:
    queue_name = "get_image"
    ttl = 10 * 60  # время жизни сообщения в секундах

    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.queue = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel(publisher_confirms=False)
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True, auto_delete=False)

    async def close(self):
        await self.connection.close()

    async def consume(self, callback, max_tasks: int):
        await self.channel.set_qos(prefetch_count=max_tasks)
        await self.queue.consume(callback)

    async def get_image(self, chat_id: int, message_id: int, user_id: int, url: str, language: str):
        data = {"chat_id": chat_id, "message_id": message_id, "user_id": user_id, "language": language, "url": url}
        message = aio_pika.Message(body=json.dumps(data).encode(), expiration=self.ttl)
        await self.channel.default_exchange.publish(message, routing_key=self.queue_name)
