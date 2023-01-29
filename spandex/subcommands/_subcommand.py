import argparse
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import spandex


class SubCommand(ABC):
    """Base class for all subcommands."""

    @abstractmethod
    def add_arguments(self, parser: Any) -> None:
        """Add arguments to the parser."""

    @abstractmethod
    def run(self, args: Any) -> None:
        """Run the subcommand."""

    @staticmethod
    def add_common_arguments(parser: Any) -> None:
        """Add common arguments to the parser."""
        parser.add_argument(
            "--verbose",
            "-v",
            action="count",
            default=0,
            help="Increase verbosity. Can be specified multiple times.",
        )
        parser.add_argument(
            "--quiet",
            "-q",
            action="count",
            default=0,
            help="Decrease verbosity. Can be specified multiple times.",
        )
        parser.add_argument(
            "--debug",
            "-d",
            action="store_true",
            help="Enable debug mode.",
        )
        parser.add_argument(
            "--version",
            "-V",
            action="version",
            version=f"spandex {spandex.__version__}",
        )

    @staticmethod
    def get_verbosity(args: Any) -> int:
        """Get the verbosity level."""
        return args.verbose - args.quiet

    @staticmethod
    def get_debug(args: Any) -> bool:
        """Get the debug mode."""
        return args.debug

    @staticmethod
    def get_verbosity_and_debug(args: Any) -> Tuple[int, bool]:
        """Get the verbosity level and debug mode."""
        return SubCommand.get_verbosity(args), SubCommand.get_debug(args)

    @staticmethod
    def get_output_path(args: Any) -> Path:
        """Get the output path."""
        return Path(args.output)

    @staticmethod
    def get_output_path_and_verbosity_and_debug(args: Any) -> Tuple[Path, int, bool]:
        """Get the output path, verbosity level, and debug mode."""
        return (
            SubCommand.get_output_path(args),
            SubCommand.get_verbosity(args),
            SubCommand.get_debug(args),
        )

    @staticmethod
    def get_output_path_and_verbosity_and_debug_and_args(
        args: Any, *args_to_keep: str
    ) -> Tuple[Path, int, bool, Dict[str, Any]]:
        """Get the output path, verbosity level, debug mode, and arguments."""
        return (
            SubCommand.get_output_path(args),
            SubCommand.get_verbosity(args),
            SubCommand
