from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json

class KafkaService:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None
        self.consumer = None

    async def start_producer(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def start_consumer(self, group_id: str):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="earliest"
        )
        await self.consumer.start()

    async def send_message(self, message: dict):
        if not self.producer:
            await self.start_producer()
        await self.producer.send_and_wait(self.topic, json.dumps(message).encode("utf-8"))

    async def consume_messages(self):
        if not self.consumer:
            await self.start_consumer(f"{self.topic}-group")
        async for msg in self.consumer:
            yield json.loads(msg.value.decode("utf-8"))

    async def close(self):
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()