"""
Module that generates and prints a tree representation of the directory structure, excluding specified patterns.
"""

import os
def generate_tree(path, gitignore_patterns):
    """
    Generates a tree representation of the directory structure starting from the given `path`.

    Args:
        path (str): The path to the root directory.
        gitignore_patterns (list): A list of patterns to exclude from the tree.

    Returns:
        dict: A dictionary representing the tree structure. The keys are the names of the files and directories,
              and the values are either `None` for files or another dictionary representing the subtree for directories.
    """
    tree = {}
    contents = os.listdir(path)

    s = set(gitignore_patterns)
    working_list = [x for x in contents if x not in s]

    for item in working_list:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            tree[item] = None
        if os.path.isdir(item_path):
            tree[item] = generate_tree(item_path, gitignore_patterns)

    return tree

def print_tree(tree, prefix=''):
    """
    Prints a tree representation of the given `tree` dictionary.

    Parameters:
        tree (dict): The dictionary representing the tree structure. The keys are the names of the files and directories,
                     and the values are either `None` for files or another dictionary representing the subtree for directories.
        prefix (str, optional): The prefix to be added to each line of the tree representation. Defaults to an empty string.

    Returns:
        None
    """
    loop = 0
    total = len(tree)

    for item, subtree in tree.items():
        p1 = '└── '
        p2 = '├── '
        p3 = '│   '
        loop = loop+1
        handle1 = p1 if loop == total else p2
        handle2 = p1 if loop == total else p3
        lineend = '/' if subtree is not None else ''
        if loop == total and subtree is not None:
            handle1 = p1
            handle2 = '    '

        icon = "🗂️  " if subtree is not None else "📄 "
        print(f"{prefix}{handle1}{icon}{item}{lineend}")
        if subtree is not None:
            print_tree(subtree, prefix + handle2)
            # print(p3)

# def sort_dict(d):
#     """ Recursively sort a dictionary and its sub-dictionaries by keys. """
#     if not isinstance(d, dict):
#         return d

#     # Recursively sort each sub-dictionary
#     return {k: sort_dict(v) for k, v in sorted(d.items())}


def sort_key(item):
    key, value = item
    key = key.lower()
    if value is None:
        return (0, key)  # Group None values first
    elif isinstance(value, dict):
        return (2, key)  # Group sub-dictionaries last
    else:
        return (1, key)  # Group other items in the middle

def sort_dict(d):
    """ Recursively sort a dictionary by custom rules and sort sub-dictionaries. """
    if not isinstance(d, dict):
        return d

    sorted_items = sorted(d.items(), key=sort_key)
    return {k: sort_dict(v) for k, v in sorted_items}

def main():
    """
    Generates a tree representation of the directory structure starting from the current directory.

    This function also reads the contents of the .gitignore file (if it exists) and extracts the patterns to exclude from the tree.
    """
    current_dir = os.getcwd()
    gitignore_patterns = []
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            for line in f:
                clean_line = line.strip().strip("/")
                if clean_line.startswith('#') or not clean_line.strip():
                    continue
                elif clean_line == '':
                    continue
                else:
                    gitignore_patterns.append(clean_line.strip())

    gitignore_patterns.append('.git')
    tree = generate_tree(current_dir, gitignore_patterns)

    # Remove this file from the tree before printing
    this_file = os.path.basename(__file__)
    del tree[this_file]

    # sort the tree
    tree = sort_dict(tree)

    # print the tree
    print_tree(tree)



if __name__ == "__main__":
    main()
