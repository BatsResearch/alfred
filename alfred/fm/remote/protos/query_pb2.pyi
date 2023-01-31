from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EncodeRequest(_message.Message):
    __slots__ = ["kwargs", "message", "reduction"]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REDUCTION_FIELD_NUMBER: _ClassVar[int]
    kwargs: str
    message: str
    reduction: str
    def __init__(self, message: _Optional[str] = ..., reduction: _Optional[str] = ..., kwargs: _Optional[str] = ...) -> None: ...

class EncodeResponse(_message.Message):
    __slots__ = ["embedding", "success"]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    embedding: bytes
    success: bool
    def __init__(self, embedding: _Optional[bytes] = ..., success: bool = ...) -> None: ...

class RunRequest(_message.Message):
    __slots__ = ["candidate", "kwargs", "message"]
    CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    candidate: str
    kwargs: str
    message: str
    def __init__(self, message: _Optional[str] = ..., candidate: _Optional[str] = ..., kwargs: _Optional[str] = ...) -> None: ...

class RunResponse(_message.Message):
    __slots__ = ["embedding", "logit", "message", "ranked", "success"]
    EMBEDDING_FIELD_NUMBER: _ClassVar[int]
    LOGIT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RANKED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    embedding: bytes
    logit: str
    message: str
    ranked: bool
    success: bool
    def __init__(self, message: _Optional[str] = ..., ranked: bool = ..., success: bool = ..., logit: _Optional[str] = ..., embedding: _Optional[bytes] = ...) -> None: ...
