from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

# as the latex file is read in as a one long string, the index of the character
# in the string is not the same as the column number in the document.  This
# function converts the index to the column number.


def get_column_number_in_document(document: List[str], index: int) -> Optional[int]:

    assert 0 <= index, f"index must be >= 0, not {index}"

    indices_passed: int = 0
    for line in document:
        if indices_passed + len(line) > index:
            return index - indices_passed + 1
        indices_passed += len(line)

    return None


def test_get_column_number_in_document() -> None:
    document: List[str] = [
        "This is a test document.",
        "It has two lines.",
    ]

    assert get_column_number_in_document(document, 0) == 1
    assert get_column_number_in_document(document, 1) == 2
    assert get_column_number_in_document(document, len(document[0]) + 4) == 5

    assert (
        get_column_number_in_document(document, len(document[0]) + len(document[1]) + 1)
        is None
    )


def get_line_number_in_document(document: List[str], index: int) -> Optional[int]:

    assert 0 <= index, f"index must be >= 0, not {index}"

    indices_passed: int = 0
    for line_number, line in enumerate(document):
        if indices_passed + len(line) > index:
            return line_number + 1
        indices_passed += len(line)

    return None


def test_get_line_number_in_document() -> None:
    document: List[str] = [
        "This is a test document.",
        "It has two lines.",
    ]

    assert get_line_number_in_document(document, 0) == 1
    assert get_line_number_in_document(document, 1) == 1
    assert get_line_number_in_document(document, len(document[0]) + 4) == 2

    assert (
        get_line_number_in_document(document, len(document[0]) + len(document[1]) + 1)
        is None
    )
