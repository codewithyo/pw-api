""" Extra functions for the project. """

from pathlib import Path
from typing import Literal


def get_all_files(
        from_: Literal['data', 'downloads'],
        type: Literal['quiz', 'assignment', 'others']
) -> list[Path]:
    """ Return all the path of JSON files present in the Folder. """
    path = Path() / from_ / type

    files = []
    for i in path.iterdir():
        if i.is_dir():
            files += [j for j in i.iterdir() if j.suffix == '.json']
        else:
            if i.suffix == '.json':
                files.append(i)
    return files
