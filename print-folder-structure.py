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
        print(f"{prefix}{handle1}{item}{lineend}")
        if subtree is not None:
            print_tree(subtree, prefix + handle2)

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
    print_tree(tree)

if __name__ == "__main__":
    main()
