from typing import *


class MarkdownTable:
    def __init__(self, headers: List[str]):
        assert headers, "Headers should not be empty"
        self.headers: List[str] = headers
        self.rows: List[List[str]] = []

    def add_row(self, row: List[str]):
        assert len(row) == len(self.headers), "Row should have the same number of elements as the header"
        self.rows.append(row)

    def _compute_widest_value_in_each_column(self) -> List[int]:
        widest = [0] * len(self.headers)
        for i, header in enumerate(self.headers):
            widest[i] = max(widest[i], len(header))
        for row in self.rows:
            for i, value in enumerate(row):
                widest[i] = max(widest[i], len(value))
        return widest

    def to_markdown(self) -> str:
        widest: List[int] = self._compute_widest_value_in_each_column()
        result: List[str] = ["|"]
        for i, header in enumerate(self.headers):
            result.append(header.ljust(widest[i]))
            result.append("|")
        result.append("\n")
        result.append("|")
        for i in range(len(self.headers)):
            result.append("-" * widest[i])
            result.append("|")
        result.append("\n")
        for row in self.rows:
            result.append("|")
            for i, value in enumerate(row):
                result.append(value.ljust(widest[i]))
                result.append("|")
            result.append("\n")
        return "".join(result)
