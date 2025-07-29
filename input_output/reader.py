from pathlib import Path
import re

def get_sorted_files(root):
    def extract_dir_no(dir_name):
        match = re.match(r"(\d+)", dir_name)
        number = (match.group(1)) # first group of re.match()
        return int(number) # convert to int before returning

    root = Path(root)
    sorted_files = []

    var_dirs = [dir for dir in root.iterdir() if dir.is_dir()]
    var_dirs = sorted(var_dirs, key=lambda dir: extract_dir_no(dir.name))

    for var_dir in var_dirs:
        deg_dirs = [dir for dir in var_dir.iterdir() if dir.is_dir()]
        deg_dirs = sorted(deg_dirs, key=lambda dir: extract_dir_no(dir.name))

        for deg_dir in deg_dirs:
            files = deg_dir.glob("*.smt2")
            sorted_files.extend(files) # append each item from the iterable separately

    return sorted_files
