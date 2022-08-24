from typing import Any

MAX_ATTEMPTS: int
logger: Any

def prompt_for_confirmation(question, default: Any | None = ..., padding: bool = ...): ...
def prompt_for_choice(choices, default: Any | None = ..., padding: bool = ...): ...
def prompt_for_input(question, default: Any | None = ..., padding: bool = ..., strip: bool = ...): ...
def prepare_prompt_text(prompt_text, **options): ...
def prepare_friendly_prompts() -> None: ...
def retry_limit(limit=...) -> None: ...

class TooManyInvalidReplies(Exception): ...
