"""Save content to a file"""


def save_to_file(content, filename):
    """Save content to a file"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print("saved to file: ", filename)
