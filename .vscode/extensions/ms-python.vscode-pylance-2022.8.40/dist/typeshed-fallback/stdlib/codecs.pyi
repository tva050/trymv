import types
from _typeshed import Self
from abc import abstractmethod
from collections.abc import Callable, Generator, Iterable
from typing import Any, BinaryIO, Protocol, TextIO
from typing_extensions import Literal

from _codecs import *

__all__ = [
    "register",
    "lookup",
    "open",
    "EncodedFile",
    "BOM",
    "BOM_BE",
    "BOM_LE",
    "BOM32_BE",
    "BOM32_LE",
    "BOM64_BE",
    "BOM64_LE",
    "BOM_UTF8",
    "BOM_UTF16",
    "BOM_UTF16_LE",
    "BOM_UTF16_BE",
    "BOM_UTF32",
    "BOM_UTF32_LE",
    "BOM_UTF32_BE",
    "CodecInfo",
    "Codec",
    "IncrementalEncoder",
    "IncrementalDecoder",
    "StreamReader",
    "StreamWriter",
    "StreamReaderWriter",
    "StreamRecoder",
    "getencoder",
    "getdecoder",
    "getincrementalencoder",
    "getincrementaldecoder",
    "getreader",
    "getwriter",
    "encode",
    "decode",
    "iterencode",
    "iterdecode",
    "strict_errors",
    "ignore_errors",
    "replace_errors",
    "xmlcharrefreplace_errors",
    "backslashreplace_errors",
    "namereplace_errors",
    "register_error",
    "lookup_error",
]

BOM32_BE: Literal[b"\xfe\xff"]
BOM32_LE: Literal[b"\xff\xfe"]
BOM64_BE: Literal[b"\x00\x00\xfe\xff"]
BOM64_LE: Literal[b"\xff\xfe\x00\x00"]

class _WritableStream(Protocol):
    def write(self, __data: bytes) -> object: ...
    def seek(self, __offset: int, __whence: int) -> object: ...
    def close(self) -> object: ...

class _ReadableStream(Protocol):
    def read(self, __size: int = ...) -> bytes: ...
    def seek(self, __offset: int, __whence: int) -> object: ...
    def close(self) -> object: ...

class _Stream(_WritableStream, _ReadableStream, Protocol): ...

# TODO: this only satisfies the most common interface, where
# bytes is the raw form and str is the cooked form.
# In the long run, both should become template parameters maybe?
# There *are* bytes->bytes and str->str encodings in the standard library.
# They were much more common in Python 2 than in Python 3.

class _Encoder(Protocol):
    def __call__(self, input: str, errors: str = ...) -> tuple[bytes, int]: ...  # signature of Codec().encode

class _Decoder(Protocol):
    def __call__(self, input: bytes, errors: str = ...) -> tuple[str, int]: ...  # signature of Codec().decode

class _StreamReader(Protocol):
    def __call__(self, stream: _ReadableStream, errors: str = ...) -> StreamReader: ...

class _StreamWriter(Protocol):
    def __call__(self, stream: _WritableStream, errors: str = ...) -> StreamWriter: ...

class _IncrementalEncoder(Protocol):
    def __call__(self, errors: str = ...) -> IncrementalEncoder: ...

class _IncrementalDecoder(Protocol):
    def __call__(self, errors: str = ...) -> IncrementalDecoder: ...

class CodecInfo(tuple[_Encoder, _Decoder, _StreamReader, _StreamWriter]):
    @property
    def encode(self) -> _Encoder: ...
    @property
    def decode(self) -> _Decoder: ...
    @property
    def streamreader(self) -> _StreamReader: ...
    @property
    def streamwriter(self) -> _StreamWriter: ...
    @property
    def incrementalencoder(self) -> _IncrementalEncoder: ...
    @property
    def incrementaldecoder(self) -> _IncrementalDecoder: ...
    name: str
    def __new__(
        cls: type[Self],
        encode: _Encoder,
        decode: _Decoder,
        streamreader: _StreamReader | None = ...,
        streamwriter: _StreamWriter | None = ...,
        incrementalencoder: _IncrementalEncoder | None = ...,
        incrementaldecoder: _IncrementalDecoder | None = ...,
        name: str | None = ...,
        *,
        _is_text_encoding: bool | None = ...,
    ) -> Self: ...

def getencoder(encoding: str) -> _Encoder: ...
def getdecoder(encoding: str) -> _Decoder: ...
def getincrementalencoder(encoding: str) -> _IncrementalEncoder: ...
def getincrementaldecoder(encoding: str) -> _IncrementalDecoder: ...
def getreader(encoding: str) -> _StreamReader: ...
def getwriter(encoding: str) -> _StreamWriter: ...
def open(
    filename: str, mode: str = ..., encoding: str | None = ..., errors: str = ..., buffering: int = ...
) -> StreamReaderWriter: ...
def EncodedFile(file: _Stream, data_encoding: str, file_encoding: str | None = ..., errors: str = ...) -> StreamRecoder: ...
def iterencode(iterator: Iterable[str], encoding: str, errors: str = ...) -> Generator[bytes, None, None]: ...
def iterdecode(iterator: Iterable[bytes], encoding: str, errors: str = ...) -> Generator[str, None, None]: ...

BOM: Literal[b"\xff\xfe", b"\xfe\xff"]  # depends on `sys.byteorder`
BOM_BE: Literal[b"\xfe\xff"]
BOM_LE: Literal[b"\xff\xfe"]
BOM_UTF8: Literal[b"\xef\xbb\xbf"]
BOM_UTF16: Literal[b"\xff\xfe", b"\xfe\xff"]  # depends on `sys.byteorder`
BOM_UTF16_BE: Literal[b"\xfe\xff"]
BOM_UTF16_LE: Literal[b"\xff\xfe"]
BOM_UTF32: Literal[b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff"]  # depends on `sys.byteorder`
BOM_UTF32_BE: Literal[b"\x00\x00\xfe\xff"]
BOM_UTF32_LE: Literal[b"\xff\xfe\x00\x00"]

def strict_errors(exception: UnicodeError) -> tuple[str | bytes, int]: ...
def replace_errors(exception: UnicodeError) -> tuple[str | bytes, int]: ...
def ignore_errors(exception: UnicodeError) -> tuple[str | bytes, int]: ...
def xmlcharrefreplace_errors(exception: UnicodeError) -> tuple[str | bytes, int]: ...
def backslashreplace_errors(exception: UnicodeError) -> tuple[str | bytes, int]: ...
def namereplace_errors(exception: UnicodeError) -> tuple[str | bytes, int]: ...

class Codec:
    # These are sort of @abstractmethod but sort of not.
    # The StreamReader and StreamWriter subclasses only implement one.
    def encode(self, input: str, errors: str = ...) -> tuple[bytes, int]: ...
    def decode(self, input: bytes, errors: str = ...) -> tuple[str, int]: ...

class IncrementalEncoder:
    errors: str
    def __init__(self, errors: str = ...) -> None: ...
    @abstractmethod
    def encode(self, input: str, final: bool = ...) -> bytes: ...
    def reset(self) -> None: ...
    # documentation says int but str is needed for the subclass.
    def getstate(self) -> int | str: ...
    def setstate(self, state: int | str) -> None: ...

class IncrementalDecoder:
    errors: str
    def __init__(self, errors: str = ...) -> None: ...
    @abstractmethod
    def decode(self, input: bytes, final: bool = ...) -> str: ...
    def reset(self) -> None: ...
    def getstate(self) -> tuple[bytes, int]: ...
    def setstate(self, state: tuple[bytes, int]) -> None: ...

# These are not documented but used in encodings/*.py implementations.
class BufferedIncrementalEncoder(IncrementalEncoder):
    buffer: str
    def __init__(self, errors: str = ...) -> None: ...
    @abstractmethod
    def _buffer_encode(self, input: str, errors: str, final: bool) -> bytes: ...
    def encode(self, input: str, final: bool = ...) -> bytes: ...

class BufferedIncrementalDecoder(IncrementalDecoder):
    buffer: bytes
    def __init__(self, errors: str = ...) -> None: ...
    @abstractmethod
    def _buffer_decode(self, input: bytes, errors: str, final: bool) -> tuple[str, int]: ...
    def decode(self, input: bytes, final: bool = ...) -> str: ...

# TODO: it is not possible to specify the requirement that all other
# attributes and methods are passed-through from the stream.
class StreamWriter(Codec):
    stream: _WritableStream
    errors: str
    def __init__(self, stream: _WritableStream, errors: str = ...) -> None: ...
    def write(self, object: str) -> None: ...
    def writelines(self, list: Iterable[str]) -> None: ...
    def reset(self) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, tb: types.TracebackType | None) -> None: ...
    def __getattr__(self, name: str, getattr: Callable[[str], Any] = ...) -> Any: ...

class StreamReader(Codec):
    stream: _ReadableStream
    errors: str
    def __init__(self, stream: _ReadableStream, errors: str = ...) -> None: ...
    def read(self, size: int = ..., chars: int = ..., firstline: bool = ...) -> str: ...
    def readline(self, size: int | None = ..., keepends: bool = ...) -> str: ...
    def readlines(self, sizehint: int | None = ..., keepends: bool = ...) -> list[str]: ...
    def reset(self) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, tb: types.TracebackType | None) -> None: ...
    def __iter__(self: Self) -> Self: ...
    def __next__(self) -> str: ...
    def __getattr__(self, name: str, getattr: Callable[[str], Any] = ...) -> Any: ...

# Doesn't actually inherit from TextIO, but wraps a BinaryIO to provide text reading and writing
# and delegates attributes to the underlying binary stream with __getattr__.
class StreamReaderWriter(TextIO):
    stream: _Stream
    def __init__(self, stream: _Stream, Reader: _StreamReader, Writer: _StreamWriter, errors: str = ...) -> None: ...
    def read(self, size: int = ...) -> str: ...
    def readline(self, size: int | None = ...) -> str: ...
    def readlines(self, sizehint: int | None = ...) -> list[str]: ...
    def __next__(self) -> str: ...
    def __iter__(self: Self) -> Self: ...
    def write(self, data: str) -> None: ...  # type: ignore[override]
    def writelines(self, list: Iterable[str]) -> None: ...
    def reset(self) -> None: ...
    def seek(self, offset: int, whence: int = ...) -> None: ...  # type: ignore[override]
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, tb: types.TracebackType | None) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    # These methods don't actually exist directly, but they are needed to satisfy the TextIO
    # interface. At runtime, they are delegated through __getattr__.
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    def truncate(self, size: int | None = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def writable(self) -> bool: ...

class StreamRecoder(BinaryIO):
    def __init__(
        self, stream: _Stream, encode: _Encoder, decode: _Decoder, Reader: _StreamReader, Writer: _StreamWriter, errors: str = ...
    ) -> None: ...
    def read(self, size: int = ...) -> bytes: ...
    def readline(self, size: int | None = ...) -> bytes: ...
    def readlines(self, sizehint: int | None = ...) -> list[bytes]: ...
    def __next__(self) -> bytes: ...
    def __iter__(self: Self) -> Self: ...
    def write(self, data: bytes) -> None: ...  # type: ignore[override]
    def writelines(self, list: Iterable[bytes]) -> None: ...
    def reset(self) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, tb: types.TracebackType | None) -> None: ...
    def seek(self, offset: int, whence: int = ...) -> None: ...  # type: ignore[override]
    # These methods don't actually exist directly, but they are needed to satisfy the BinaryIO
    # interface. At runtime, they are delegated through __getattr__.
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    def truncate(self, size: int | None = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def writable(self) -> bool: ...
