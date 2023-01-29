#!/usr/bin/env python

import os
import sys
from typing import List

# A list to store the names of the files visited
files_visited: List[str] = []

# Recursive function to parse a LaTeX file for \input commands


# def parse_latex_file(filename: str) -> None:
#     # Open the file
#     with open(filename, "r") as f:
#         # Read the file line by line
#         for line in f:
#             # Check if the line contains an \input command
#             if "\\input{" in line:
#                 # Get the name of the file specified in the \input command
#                 input_file = line.strip().split("{")[1].split("}")[0]
#                 # print(f"Found input file: {input_file}")
#                 # if the file does not have a .tex extension, add it
#                 if not input_file.endswith(".tex"):
#                     input_file += ".tex"

#                 # Check if the file exists
#                 if not os.path.exists(input_file):
#                     # If the file does not exist, print an error message and exit the script
#                     print(f"Error: File {input_file} does not exist")
#                     sys.exit(1)
#                 # If the file does exist, add it to the list of files visited
#                 files_visited.append(input_file)
#                 # Recursively parse the input file
#                 parse_latex_file(input_file)


# Recursive function to parse a LaTeX file for \input commands
def parse_latex_file(filename: str) -> None:
    # Open the file
    with open(filename, "r") as f:
        # Read the file line by line
        for line in f:
            # Check if the line contains an \input command
            if "\\input{" in line:
                # Get the name of the file specified in the \input command
                input_file = line.strip().split("{")[1].split("}")[0]
                # Check if the file exists
                if not os.path.exists(input_file):
                    # If the file does not exist, print an error message and exit the script
                    print(f"Error: File {input_file} does not exist")
                    sys.exit(1)
                # If the file does exist, add it to the list of files visited
                files_visited.append(input_file)
                # Recursively parse the input file
                parse_latex_file(input_file)
            else:
                # If the line does not contain an \input command, write it to the output file
                with open("output.tex", "a") as out:
                    out.write(line)


# Main function


def main() -> None:
    # Check if a filename was provided as an argument
    if len(sys.argv) < 2:
        print("Error: No file specified")
        sys.exit(1)
    # Get the filename from the command line arguments
    filename = sys.argv[1]
    # Check if the file exists
    if not os.path.exists(filename):
        print(f"Error: File {filename} does not exist")
        sys.exit(1)
    # Add the initial file to the list of files visited
    files_visited.append(filename)
    # Parse the initial file for \input commands
    parse_latex_file(filename)
    # Print the list of files visited
    for file in files_visited:
        print(file)


# Run the main function
if __name__ == "__main__":
    main()
