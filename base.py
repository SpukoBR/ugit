import os
import json

from . import data

def write_tree(directory='.'):
    with os.scandir(directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'
            if entry.is_file(follow_symlinks=False):
                with open(full, 'rb') as f:
                    oid = data.hash_object(f.read())
                print(f'File {full} stored as object {oid}')
            elif entry.is_dir(follow_symlinks=False):
                write_tree(full)

    tree_entries = []
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file(follow_symlinks=False):
                with open(f'{directory}/{entry.name}', 'rb') as f:
                    oid = data.hash_object(f.read())
                tree_entries.append({'type': 'blob', 'name': entry.name, 'oid': oid})
            elif entry.is_dir(follow_symlinks=False):
                oid = write_tree(f'{directory}/{entry.name}')
                tree_entries.append({'type': 'tree', 'name': entry.name, 'oid': oid})
    
    tree = json.dumps(tree_entries)
    tree_oid = data.hash_object(tree.encode(), 'tree')
    print(f'Tree object created with OID {tree_oid}')
    return tree_oid
