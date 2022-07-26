from xrmfilecleaner.qt import *
import time
import os
from pathlib import Path
from datetime import datetime


class FileScraper(QObject):
    finished = pyqtSignal()

    def __init__(self, dirs, exm_occ: bool, exm: bool, max_age: int):
        super().__init__()
        self.dirs = dirs
        self.exm = exm
        self.exm_occ = exm_occ
        self.max_age = max_age

    def start(self):
        filters = []
        if self.exm:
            filters.append(".txm-exm")
        if self.exm_occ:
            filters.append(".txm-exm-occ")

        for curr_dir in self.dirs:
            for root, subdirs, files in os.walk(curr_dir):
                for file in files:
                    path = Path(root) / file
                    if path.suffix in filters:
                        creation = datetime.fromtimestamp(path.stat().st_ctime)
                        age_days = (datetime.now() - creation).total_seconds()/60/60/24

                        if age_days > self.max_age:
                            print(path, creation, age_days)

        for i in range(5):
            print(i)
            time.sleep(1)

        self.finished.emit()
