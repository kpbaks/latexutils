#!/usr/bin/env python3

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import epilog
import latex
from pygments import highlight
from pygments.lexers import TexLexer
from pygments.formatters import TerminalFormatter

DESCRIPTION = """\
Count the number of times each reference is used in a LaTeX document.
"""

EPILOG = """\
The output is a list of references, one per line, with the number of times
each reference is used in the document.  The references are sorted by the
number of times they are used, with the most used references first.
"""

from utils import get_column_number_in_document, get_line_number_in_document


@dataclass
class TextFileInterval:
    line_start: int
    line_end: int
    column_start: int
    column_end: int

    def __str__(self) -> str:
        return (
            f"{self.line_start}:{self.column_start}-{self.line_end}:{self.column_end}"
        )

    def get_start(self) -> Tuple[int, int]:
        return (self.line_start, self.column_start)

    def get_end(self) -> Tuple[int, int]:
        return (self.line_end, self.column_end)


@dataclass
class LaTeXLabel:
    label: str
    file: str
    interval: TextFileInterval
    text: str = ""

    def __str__(self) -> str:
        return f"{self.label} ({self.file}:{self.interval})"

    def __hash__(self) -> int:
        return hash(self.label + self.file + str(self.interval))


@dataclass
class LaTeXReference:
    """A LaTeX reference.

    Attributes:
        name: The name of the reference.
        count: The number of times the reference is used.
    """
    
    file: str
    interval: TextFileInterval = None
    label_reffered_to: Optional[LaTeXLabel] = None
    text: str = ""


def red(text: str) -> str:
    return f"\033[1;31m{text}\033[0m"


def green(text: str) -> str:
    return f"\033[1;32m{text}\033[0m"


def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


def italics(text: str) -> str:
    return f"\033[3m{text}\033[0m"


def ellipsis(text: str, max_length: int) -> str:
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text



def find_in_list(
    lst: List[Any], value: Any, comparator: Callable[Any, bool] = lambda a, b: a == b
) -> Optional[Any]:
    """Find a value in a list.

    Args:
        lst: The list to search.
        value: The value to search for.

    Returns:
        The first value in the list that is equal to the value searched for.
        If no such value is found, returns None.
    """
    for item in lst:
        # print(f"item: {item}, v# alue: {value}")
        if comparator(item, value):
            return item
    return None


if __name__ == "__main__":

    name_of_this_script: str = os.path.basename(__file__)

    parser = argparse.ArgumentParser(
        prog=name_of_this_script, description=DESCRIPTION, epilog=EPILOG
    )
    parser.add_argument(
        "filename",
        help="the LaTeX file to process. If the filename is '-', then the file is read from standard input.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="check that the references are valid.  If this option is not given, then the references are not checked.",
    )

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase verbosity"
    )
    parser.add_argument(
        "-vv", "--very-verbose", action="count", default=0, help="increase verbosity"
    )
    parser.add_argument(
        "-vvv",
        "--very-very-verbose",
        action="count",
        default=0,
        help="increase verbosity",
    )
    parser.add_argument(
        "-q", "--quiet", action="count", default=0, help="decrease verbosity"
    )

    args = parser.parse_args()

    # Read the file
    text: str = ""
    try:
        with open(args.filename, "r") as f:
            text = f.read()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    labels: List[LaTeXLabel] = []
    references: List[LaTeXReference] = []

    document: List[str] = text.splitlines()
    # print(f"document has {len(document)} lines")
    # n_grahemes: int = sum([len(line) for line in document])
    # print(f"document has {n_grahemes} grahemes")
    # print(document)

    for line_number, line in enumerate(document):
        line_number += 1  # line numbers start at 1

        hit: Optional[re.Match] = re.search(r"\\label\{(?P<label>[^}]+)\}", line)
        if hit:
            label: str = hit.group("label")
            line_start: int = line_number
            line_end: int = line_number
            column_start: int = hit.start("label")
            column_end: int = hit.end("label")
            interval: TextFileInterval = TextFileInterval(line_start, line_end, column_start, column_end)
            labels.append(LaTeXLabel(label, args.filename, interval, text=line))



    for line_number, line in enumerate(document):
        line_number += 1  # line numbers start at 1
        hit: Optional[re.Match] = re.search(r"\\.*ref\{(?P<label>[^}]+)\}", line)
        if hit:
            label: str = hit.group("label")
            line_start: int = line_number
            line_end: int = line_number
            column_start: int = hit.start("label")
            column_end: int = hit.end("label")
            interval: TextFileInterval = TextFileInterval(line_start, line_end, column_start, column_end)
            label_reffered_to_or_none: Optional[LaTeXLabel] = find_in_list(labels, label, lambda a, b: a.label == b)
            references.append(LaTeXReference(args.filename, interval, label_reffered_to_or_none, text=line))

    label_counts: Dict[LaTeXLabel, int] = {label: 0 for label in labels}

    for label in references:
        if label.label_reffered_to is None:
            continue

        label_counts[label.label_reffered_to] += 1

    for label, count in sorted(
        label_counts.items(), key=lambda item: item[1], reverse=True
    ):
        line_start, column_start = label.interval.get_start()
        referened: bool = count > 0

        if not referened:
            url: str = f"{label.file}:{line_start}:{column_start}"
            # print the label int red, and show where it is defined
            print(f"{red(label.label)} (defined at {bold(url)}) is {red('NOT')} referenced!")
        else:
            # print the label in green, and show where it is defined
            # for each reference, show where it is used
            url: str = f"{label.file}:{line_start}:{column_start}"

            print(f"{green(label.label)} (defined at {bold(url)}) is referenced {green(count)} times:")
            for reference in references:
                if reference.label_reffered_to is None:
                    continue
                if reference.label_reffered_to == label:
                    line_start, column_start = reference.interval.get_start()

                    text: str = reference.text
                    text = text.replace("\\", "")

                    terminal_width: int = os.get_terminal_size().columns
                    text_elipsized: str = ellipsis(text, terminal_width - 10)
                    text_highlighted: str = highlight(text_elipsized, TexLexer(), TerminalFormatter())

                    url: str = f"{reference.file}:{line_start}:{column_start}"
                    # print(f"    {bold(url)}: {italics(text_elipsized)}")
                    # print(f"    {bold(url)}: {text_highlighted}")
                    print(f"    {bold(url)}:")
                    print(f"        {text_highlighted}")

        print()
