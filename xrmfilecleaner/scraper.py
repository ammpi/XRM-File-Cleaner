from xrmfilecleaner.qt import *
import time
import os
from pathlib import Path
from datetime import datetime
from xrmfilecleaner.logger import log
from send2trash import send2trash


class FileScanner(QObject):
    finished = pyqtSignal()

    def __init__(self, dirs, exm_occ: bool, exm: bool, max_age: int, test=False):
        super().__init__()
        self.dirs = dirs
        self.exm = exm
        self.exm_occ = exm_occ
        self.max_age = max_age
        self.test = test

    def start(self):
        log.info("Starting scan")
        filters = []
        if self.test is True:
            log.info("Running test scan, no files will be deleted")
        if self.exm:
            log.info("Delete .txm-exm is enabled")
            filters.append(".txm-exm")
        if self.exm_occ:
            log.info("Delete .txm-exm-ooc is enabled")
            filters.append(".txm-exm-ooc")

        if len(filters) == 0:
            log.info("Neither .txm-exm or .txm-exm-ooc are enabled for deletion")

        to_delete = []

        for curr_dir in self.dirs:
            for root, subdirs, files in os.walk(curr_dir):
                for file in files:
                    path = Path(root) / file
                    if path.suffix in filters:
                        creation = datetime.fromtimestamp(path.stat().st_ctime)
                        age_days = (datetime.now() - creation).total_seconds()/60/60/24

                        if age_days > self.max_age:

                            print(path, creation, age_days)
                            to_delete.append(path)
                            log.info("Found file to delete: ")

        if self.test is False:
            for file in to_delete:
                try:
                    # send2trash(file)
                except Exception as err:
                    log.error("Failed to delte file", type(err), err, err.__traceback__)

        self.finished.emit()
        log.info("Finished scan")
