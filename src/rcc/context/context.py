from src.rcc.error.error import Error

class Context:
    file: str
    content: str

    def __init__(self, path: str) -> None:
        with open(path, "r") as file:
            self.file = path
            self.content = file.read()

            if len(self.content) == 0:
                self.error((0, 0), f"file '{path}' is empty")

            file.close()

    def error(self, pos: tuple[int, int], message: str) -> None:
        e: Error = Error(self.file, *pos, message)

        print(e)
        exit(1)