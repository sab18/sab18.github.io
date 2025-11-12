import os
import re
import sys

def rename_figures(project, operation, value):
    main_folder = "assets/images"
    folder = os.path.join(main_folder, project)
    # Regex matches Fig_1.png, Fig_1_a.jpg, Fig_10_b.webp, etc.
    pattern = re.compile(r"^Fig_(\d+)(?:_([a-zA-Z]))?(\.[a-zA-Z0-9]+)$")
    files = []
    for fname in os.listdir(folder):
        match = pattern.match(fname)
        if match:
            num = int(match.group(1))
            letter = match.group(2) or ""
            ext = match.group(3)
            files.append((num, letter, ext, fname))
    if operation == "add":
        files = [f for f in files if f[0] >= value]
        files.sort(reverse=True)
        delta = 1
    elif operation == "subtract":
        files = [f for f in files if f[0] <= value]
        files.sort()
        delta = -1
    else:
        print("Operation must be 'add' or 'subtract'")
        return
    for num, letter, ext, fname in files:
        new_num = num + delta
        new_name = f"Fig_{new_num}"
        if letter:
            new_name += f"_{letter}"
        new_name += ext
        old_path = os.path.join(folder, fname)
        new_path = os.path.join(folder, new_name)
        print(f"Renaming {fname} -> {new_name}")
        os.rename(old_path, new_path)

if __name__ == "__main__":
    project = "table"  # e.g., 'table', 'dresser', etc.
    operation = "add"  # or 'subtract'
    value = 3           # threshold value
    rename_figures(project, operation, value)