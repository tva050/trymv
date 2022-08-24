from typing import Any, Iterable

from google.protobuf.descriptor import Descriptor
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import Message

class MessageFactory:
    pool: Any
    def __init__(self, pool: DescriptorPool | None = ...) -> None: ...
    def GetPrototype(self, descriptor: Descriptor) -> type[Message]: ...
    def GetMessages(self, files: Iterable[str]) -> dict[str, type[Message]]: ...

def GetMessages(file_protos: Iterable[FileDescriptorProto]) -> dict[str, type[Message]]: ...
