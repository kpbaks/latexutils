def merge(filename: str) -> str:
    try:
        with open(filename, "r") as f:
            text = f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File {filename} does not exist") from e
