import pathlib
import subprocess
import tempfile
from datetime import datetime, timedelta
from typing import *

from get_directory_size import get_directory_size

FORMATS: List[str] = [
    "--bzip2",
    "--xz",
    "--lzip",
    "--lzma",
    "--lzop",
    "--gzip",
    "--zstd",
]


class Result:
    def __init__(self, algorithm: str, ratio: float, time_taken: timedelta):
        self.algorithm = algorithm
        self.ratio = ratio
        self.time_taken = time_taken

    def to_markdown_row(self):
        return f"{self.algorithm}|{self.ratio:.3%}|{self.time_taken}"


def main():
    for directory in filter(lambda entry: entry.is_dir(), pathlib.Path("./Data/").iterdir()):
        original_size = get_directory_size(str(directory))
        results = []
        print(f"Original size is {original_size:,} B")
        for compression_format in FORMATS:
            with tempfile.NamedTemporaryFile() as named_temporary_file:
                command = ["tar", "--preserve-permissions", compression_format, "--create", "--file", named_temporary_file.name, str(directory)]
                print("Running", " ".join(command))
                start_datetime = datetime.now()
                subprocess.check_output(command)
                compressed_size = pathlib.Path(named_temporary_file.name).stat().st_size
                ratio = compressed_size / original_size
                time_taken = datetime.now() - start_datetime
                print(f"{compression_format} compressed the file to {ratio:.3%} of its original size in {time_taken}.")
                results.append(Result(compression_format, ratio, time_taken))
        markdown_filename = f"{directory.name}.md"
        with open(markdown_filename, "w") as markdown_file_handle:
            for result in results:
                markdown_file_handle.write(result.to_markdown_row() + "\n")
        print(f"Wrote Markdown table to {markdown_filename}.")


if __name__ == "__main__":
    main()
