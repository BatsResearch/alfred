from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HandshakeRequest(_message.Message):
    __slots__ = ("client_id",)
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    def __init__(self, client_id: _Optional[str] = ...) -> None: ...

class HandshakeResponse(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...

class RunRequest(_message.Message):
    __slots__ = ("message", "candidate", "kwargs")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    message: str
    candidate: str
    kwargs: str
    def __init__(self, message: _Optional[str] = ..., candidate: _Optional[str] = ..., kwargs: _Optional[str] = ...) -> None: ...

class RunResponse(_message.Message):
    __slots__ = ("message", "ranked", "success", "logit", "embedding")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RANKED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    LOGIT_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    message: str
    ranked: bool
    success: bool
    logit: str
    embedding: bytes
    def __init__(self, message: _Optional[str] = ..., ranked: bool = ..., success: bool = ..., logit: _Optional[str] = ..., embedding: _Optional[bytes] = ...) -> None: ...

class EncodeRequest(_message.Message):
    __slots__ = ("message", "reduction", "kwargs")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REDUCTION_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    message: str
    reduction: str
    kwargs: str
    def __init__(self, message: _Optional[str] = ..., reduction: _Optional[str] = ..., kwargs: _Optional[str] = ...) -> None: ...

class EncodeResponse(_message.Message):
    __slots__ = ("embedding", "success")
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    embedding: bytes
    success: bool
    def __init__(self, embedding: _Optional[bytes] = ..., success: bool = ...) -> None: ...
