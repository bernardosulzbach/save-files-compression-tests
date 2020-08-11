import pathlib
import subprocess
import tempfile
from datetime import datetime, timedelta
from typing import *

import matplotlib.pyplot as plt


from get_directory_size import get_directory_size
from markdown_table import MarkdownTable

PATH_TO_DATA = "data"
PATH_TO_GENERATED = "generated"

ALGORITHMS: List[str] = [
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
        self.algorithm: str = algorithm
        self.ratio: float = ratio
        self.time_taken: timedelta = time_taken

    def to_string_list(self) -> List[str]:
        return [self.algorithm, f"{self.ratio:.3%}", str(self.time_taken / timedelta(seconds=1))]


def write_results_table(results: List[Result], markdown_filename: str):
    markdown_table = MarkdownTable(["Algorithm", "Compression ratio", "Time taken (s)"])
    for result in results:
        markdown_table.add_row(result.to_string_list())
    with open(markdown_filename, "w") as markdown_file_handle:
        markdown_file_handle.write(markdown_table.to_markdown())
    print(f"Wrote Markdown table to {markdown_filename}.")


def plot_results(results: List[Result], filename: str):
    fig, ax = plt.subplots()
    for result in results:
        x = result.ratio
        y = result.time_taken / timedelta(seconds=1)
        ax.plot(x, y, "o", label=result.algorithm)
        # Could annotate, but this causes overlaps that matplotlib does not fix.
        # ax.annotate(result.algorithm, (x, y))
    ax.legend()
    ax.set_xlabel("Compression ratio (lower is better)")
    ax.set_ylabel("Time taken (s) (lower is better)")
    fig.savefig(filename)


def main():
    for directory in filter(lambda entry: entry.is_dir(), pathlib.Path(PATH_TO_DATA).iterdir()):
        original_size = get_directory_size(str(directory))
        results = []
        print(f"Original size is {original_size:,} B.")
        for algorithm in ALGORITHMS:
            with tempfile.NamedTemporaryFile() as named_temporary_file:
                command = ["tar", "--preserve-permissions", algorithm, "--create", "--file", named_temporary_file.name, str(directory)]
                print("Running", " ".join(command))
                start_datetime = datetime.now()
                subprocess.check_output(command)
                compressed_size = pathlib.Path(named_temporary_file.name).stat().st_size
                ratio = compressed_size / original_size
                time_taken = datetime.now() - start_datetime
                print(f"{algorithm} compressed the file to {ratio:.3%} of its original size in {time_taken}.")
                results.append(Result(algorithm.strip("--"), ratio, time_taken))
        results.sort(key=lambda r: r.ratio)
        markdown_filename = f"{PATH_TO_GENERATED}/{directory.name}.md"
        write_results_table(results, markdown_filename)
        plot_filename = f"{PATH_TO_GENERATED}/{directory.name}.svg"
        plot_results(results, plot_filename)


if __name__ == "__main__":
    main()
