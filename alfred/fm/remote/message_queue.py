import asyncio
import uuid
from typing import Dict, List, Any


class Message:
    def __init__(self, topic: str, content: Any, session_id: str):
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.content = content
        self.session_id = session_id


class Topic:
    def __init__(self, name: str):
        self.name = name
        self.messages = asyncio.Queue()
        self.subscribers: List[str] = []


class MessageBroker:
    def __init__(self):
        self.topics: Dict[str, Topic] = {}
        self.sessions: Dict[str, asyncio.Queue] = {}

    def create_topic(self, topic_name: str) -> Topic:
        if topic_name not in self.topics:
            self.topics[topic_name] = Topic(topic_name)
        return self.topics[topic_name]

    def subscribe(self, topic_name: str, session_id: str):
        topic = self.create_topic(topic_name)
        if session_id not in topic.subscribers:
            topic.subscribers.append(session_id)

    async def publish(self, message: Message):
        topic = self.create_topic(message.topic)
        await topic.messages.put(message)
        for session_id in topic.subscribers:
            if session_id in self.sessions:
                await self.sessions[session_id].put(message)

    async def consume(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = asyncio.Queue()
        return await self.sessions[session_id].get()
