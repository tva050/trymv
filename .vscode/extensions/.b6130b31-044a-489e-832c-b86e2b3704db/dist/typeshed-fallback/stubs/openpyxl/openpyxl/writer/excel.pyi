from typing import Any

class ExcelWriter:
    workbook: Any
    manifest: Any
    vba_modified: Any
    def __init__(self, workbook, archive) -> None: ...
    def write_data(self) -> None: ...
    def write_worksheet(self, ws) -> None: ...
    def save(self) -> None: ...

def save_workbook(workbook, filename): ...
def save_virtual_workbook(workbook): ...
