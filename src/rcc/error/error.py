from os import getcwd
from dataclasses import dataclass

@dataclass
class Error:
    file: str
    line: int
    column: int
    message: str

    def __str__(self) -> str:
        ansi_red: str = "\u001b[31m"
        ansi_reset: str = "\u001b[0m"
        current_dir: str = getcwd().replace("\\", "/")

        error_msg = [
            f"{ansi_red}-> ERROR: {self.message}",
            f"    at {current_dir}/{self.file}:{self.line + 1}:{self.column + 1}{ansi_reset}",
        ]

        return "\n".join(error_msg)
    
    def __repr__(self) -> str:
        return self.__str__()