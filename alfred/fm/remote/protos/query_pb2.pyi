from typing import ClassVar as _ClassVar, Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor


class DataHeaderRequest(_message.Message):
    __slots__ = ["data_meta", "data_size"]
    DATA_META_FIELD_NUMBER: _ClassVar[int]
    DATA_SIZE_FIELD_NUMBER: _ClassVar[int]
    data_meta: str
    data_size: int

    def __init__(self, data_meta: _Optional[str] = ..., data_size: _Optional[int] = ...) -> None: ...


class DataHeaderResponse(_message.Message):
    __slots__ = ["data_meta", "data_size"]
    DATA_META_FIELD_NUMBER: _ClassVar[int]
    DATA_SIZE_FIELD_NUMBER: _ClassVar[int]
    data_meta: str
    data_size: int

    def __init__(self, data_meta: _Optional[str] = ..., data_size: _Optional[int] = ...) -> None: ...


class DataReadySignal(_message.Message):
    __slots__ = ["data_size", "kwargs"]
    DATA_SIZE_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    data_size: int
    kwargs: str

    def __init__(self, data_size: _Optional[int] = ..., kwargs: _Optional[str] = ...) -> None: ...


class InferenceRequest(_message.Message):
    __slots__ = ["candidate", "kwargs", "message"]
    CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    KWARGS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    candidate: str
    kwargs: str
    message: str

    def __init__(self, message: _Optional[str] = ..., candidate: _Optional[str] = ...,
                 kwargs: _Optional[str] = ...) -> None: ...


class InferenceResponse(_message.Message):
    __slots__ = ["logit", "message", "ranked", "success"]
    LOGIT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RANKED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    logit: str
    message: str
    ranked: bool
    success: bool

    def __init__(self, message: _Optional[str] = ..., ranked: bool = ..., success: bool = ...,
                 logit: _Optional[str] = ...) -> None: ...
