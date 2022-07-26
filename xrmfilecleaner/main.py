from xrmfilecleaner.qt import *
from xrmfilecleaner import ui
from datetime import datetime, time
from pathlib import Path
from scraper import FileScraper

import sys


def scan():
    thread = QThread()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("XRM File Cleaner")
    app.setOrganizationDomain("AMMPI")
    app.setOrganizationName("AMMPI")

    tray = ui.StatusWidget()
    tray.show()

    settings = ui.SettingsDialog()

    menu = QMenu()
    show_settings = QAction()
    show_settings.setText("Settings")
    show_settings.triggered.connect(settings.show)
    menu.addAction(show_settings)

    quit = QAction()
    quit.triggered.connect(app.exit)
    quit.setText("Quit")
    menu.addAction(quit)

    tray.setContextMenu(menu)

    class TimerTimout(QObject):
        def __init__(self):
            super().__init__()

            self.scan_thread = QThread()
            self.scan_worker = None

        def onTimeOut(self):
            scan_time = settings.scan_time.time()
            curr = QTime.currentTime()
            curr.setHMS(curr.hour(), curr.minute(), curr.second(), 0)
            x = settings.dirs_list.toPlainText().split("\n")
            if scan_time == curr:
                print(scan_time)
                print("yes")

                txt = settings.dirs_list.toPlainText().split("\n")
                dirs = [Path(i) for i in txt]

                self.scan_worker = FileScraper(
                    dirs,
                    settings.exm_ooc_check.isChecked(),
                    settings.exm_check.isChecked(),
                    settings.interval_edit.value()
                )
                self.scan_worker.moveToThread(self.scan_thread)
                self.scan_thread.finished.connect(self.scan_worker.deleteLater)
                self.scan_thread.started.connect(self.scan_worker.start)
                self.scan_worker.finished.connect(self.onFinished)
                self.scan_thread.start()

            else:
                print("no")

        def onFinished(self):
            self.scan_thread.quit()
            self.scan_thread.wait()

    timout = TimerTimout()

    timer = QTimer()
    timer.timeout.connect(timout.onTimeOut)
    timer.start(1000)

    sys.exit(app.exec())

