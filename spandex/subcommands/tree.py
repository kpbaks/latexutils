from spandex.subcommands._subcommand import SubCommand


class Tree(SubCommand):
    """Print the input tree."""

    def add_arguments(self, parser: Any) -> None:
        """Add arguments to the parser."""
        parser.add_argument("filename", help="the LaTeX file to parse")

    def run(self, args: Any) -> None:
        """Run the subcommand."""
        filename = args.filename
        verbosity, debug = self.get_verbosity_and_debug(args)
