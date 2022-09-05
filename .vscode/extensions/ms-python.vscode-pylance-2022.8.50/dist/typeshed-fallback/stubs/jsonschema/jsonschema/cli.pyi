from typing import Any

class _CannotLoadFile(Exception): ...

class _Outputter:
    def __init__(self, formatter, stdout, stderr): ...
    @classmethod
    def from_arguments(cls, arguments, stdout, stderr): ...
    def load(self, path): ...
    def filenotfound_error(self, **kwargs) -> None: ...
    def parsing_error(self, **kwargs) -> None: ...
    def validation_error(self, **kwargs) -> None: ...
    def validation_success(self, **kwargs) -> None: ...

class _PrettyFormatter:
    def filenotfound_error(self, path, exc_info): ...
    def parsing_error(self, path, exc_info): ...
    def validation_error(self, instance_path, error): ...
    def validation_success(self, instance_path): ...

class _PlainFormatter:
    def __init__(self, error_format): ...
    def filenotfound_error(self, path, exc_info): ...
    def parsing_error(self, path, exc_info): ...
    def validation_error(self, instance_path, error): ...
    def validation_success(self, instance_path): ...

parser: Any

def parse_args(args): ...
def main(args=...) -> None: ...
def run(arguments, stdout=..., stderr=..., stdin=...): ...
