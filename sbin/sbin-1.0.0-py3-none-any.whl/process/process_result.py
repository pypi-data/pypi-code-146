from pydantic import BaseModel


class ProcessResult(BaseModel):
    exit_code: int
    stdout: str = ""
    stderr: str = ""

    def has_succeeded(self) -> bool:
        return self.exit_code == 0

    def has_failed(self) -> bool:
        return not self.has_succeeded()
