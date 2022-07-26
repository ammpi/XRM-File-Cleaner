from pathlib import Path
import os
from xrmfilecleaner.qt import *


_this = Path(os.path.abspath(__file__))
_resource_path = _this.parent / "resources"
_img_ext = (".png", ".svg")


def get_resource(file: str):
    path = _resource_path / file
    print(path, path.suffix)
    if any(path.suffix == i for i in _img_ext):
        return QIcon(str(path))
    else:
        raise ValueError("Could not determine what to do with file")
