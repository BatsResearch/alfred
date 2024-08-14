# Message Queue

[Alfred Index](../../../README.md#alfred-index) /
[Alfred](../../index.md#alfred) /
[Fm](../index.md#fm) /
[Remote](./index.md#remote) /
Message Queue

> Auto-generated documentation for [alfred.fm.remote.message_queue](../../../../alfred/fm/remote/message_queue.py) module.

- [Message Queue](#message-queue)
  - [Message](#message)
  - [MessageBroker](#messagebroker)
    - [MessageBroker().consume](#messagebroker()consume)
    - [MessageBroker().create_topic](#messagebroker()create_topic)
    - [MessageBroker().publish](#messagebroker()publish)
    - [MessageBroker().subscribe](#messagebroker()subscribe)
  - [Topic](#topic)

## Message

[Show source in message_queue.py:6](../../../../alfred/fm/remote/message_queue.py#L6)

#### Signature

```python
class Message:
    def __init__(self, topic: str, content: Any, session_id: str):
        ...
```



## MessageBroker

[Show source in message_queue.py:21](../../../../alfred/fm/remote/message_queue.py#L21)

#### Signature

```python
class MessageBroker:
    def __init__(self):
        ...
```

### MessageBroker().consume

[Show source in message_queue.py:43](../../../../alfred/fm/remote/message_queue.py#L43)

#### Signature

```python
async def consume(self, session_id: str):
    ...
```

### MessageBroker().create_topic

[Show source in message_queue.py:26](../../../../alfred/fm/remote/message_queue.py#L26)

#### Signature

```python
def create_topic(self, topic_name: str) -> Topic:
    ...
```

#### See also

- [Topic](#topic)

### MessageBroker().publish

[Show source in message_queue.py:36](../../../../alfred/fm/remote/message_queue.py#L36)

#### Signature

```python
async def publish(self, message: Message):
    ...
```

#### See also

- [Message](#message)

### MessageBroker().subscribe

[Show source in message_queue.py:31](../../../../alfred/fm/remote/message_queue.py#L31)

#### Signature

```python
def subscribe(self, topic_name: str, session_id: str):
    ...
```



## Topic

[Show source in message_queue.py:14](../../../../alfred/fm/remote/message_queue.py#L14)

#### Signature

```python
class Topic:
    def __init__(self, name: str):
        ...
```


