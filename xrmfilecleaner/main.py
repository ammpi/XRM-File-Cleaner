from xrmfilecleaner.qt import *
from xrmfilecleaner import ui
from xrmfilecleaner import __version__
from pathlib import Path
from scraper import FileScanner
from xrmfilecleaner.logger import log


import sys


def excepthook(excType, excValue, traceback):
    log.error("Uncaught exception", exc_info=(excType, excValue, traceback))


sys.excepthook = excepthook


def _update_stylesheet():
    ss = ""
    ss += "QMenu {background: white; margin: 0px; border: 1px solid lightgrey;}"
    ss += "QMenu::separator {height: 1px; background: lightgray; margin-left: 25px; margin-right: 5px;}"
    ss += "QMenu::item:selected {background: rgb(153, 209, 255); color: black}"

    # Toolbars
    ss += "QToolBar {background-color: white; padding: 3px; spacing: 3px}"
    ss += "QToolBar::separator {background: rgb(250, 250, 250); margin-left: 5px; margin-right: 5px;}"

    # QLineEdit
    ss += "QLineEdit {padding: 2px 2px}"
    ss += "QDateEdit {padding: 2px 2px}"

    # Dock widgets
    ss += "QDockWidget {border: 1px solid lightgrey; font-family: Segoe UI}"
    ss += "QDockWidget::title {background: white; margin-top:5px; text-align: center; padding-bottom: 3px}"

    # Pushbutton
    ss += "QPushButton {background: rgb(242, 242, 242); border-style: solid; border-width: 1px; border-color: lightgrey; border-radius: 1px; padding: 4px 6px 4px 6px}"
    ss += "QPushButton::hover {background: #e5f3ff; border-color: #cce8ff}"
    ss += "QPushButton::checked {background: #cae6ff; border-color: #94ceff}"
    ss += "QPushButton::focus {border-color: #94ceff}"
    ss += "QPushButton::disabled {background: #d7d7d7; border-color: #cacaca}"
    ss += "QToolButton {padding: 2px 2px 2px 2px}"

    # QComboBox
    ss += "QComboBox {background: rgb(245, 245, 245); border-style: solid; border-width: 1px; border-color: rgb(210, 210, 210); border-radius: 1px; padding: 2px 8px 2px 8px}"
    ss += "QComboBox::hover {background: #e5f3ff; border-color: #cce8ff}"
    ss += "QComboBox::down-arrow {image: url(images:downarrow.svg); width: 12px; height: 12px}"
    ss += "QComboBox::drop-down {border: 0px}"
    ss += "QSpinBox {padding: 1px 4px 2px 2px}"
    ss += "QDoubleSpinBox {border-color: blue; padding: 1px 4px 2px 2px}"
    ss += "QCheckBox::indicator {width: 17; height: 17}"
    ss += "QHeaderView {height: 20px}"
    app.setStyleSheet(ss)

    pal = app.palette()
    col = Qt.white
    pal.setColor(QPalette.Window, col)
    pal.setColor(QPalette.Base, col)
    app.setPalette(pal)
    font = QFont()
    font.setFamily("Segoe UI")


if __name__ == "__main__":
    log.info(f"Starting XRM file cleaner v{__version__}")
    app = QApplication(sys.argv)
    app.setApplicationName("XRM File Cleaner")
    app.setOrganizationDomain("AMMPI")
    app.setOrganizationName("AMMPI")

    app.setQuitOnLastWindowClosed(False)

    tray = ui.StatusWidget()
    tray.show()

    settings = ui.SettingsDialog()

    menu = QMenu()
    show_settings = QAction()
    show_settings.setText("Settings")
    show_settings.triggered.connect(settings.show)
    menu.addAction(show_settings)

    _update_stylesheet()

    tray.setContextMenu(menu)

    class TimerTimout(QObject):
        def __init__(self):
            super().__init__()

            self.scan_thread = QThread()
            self.scan_worker = None

        def onTimeout(self, test=False):
            scan_time = settings.scan_time.time()
            curr = QTime.currentTime()
            curr.setHMS(curr.hour(), curr.minute(), curr.second(), 0)

            if scan_time == curr or test is True:
                print(scan_time)
                print("yes")

                txt = settings.dirs_list.toPlainText().split("\n")
                dirs = [Path(i) for i in txt]

                self.scan_worker = FileScanner(
                    dirs,
                    settings.exm_ooc_check.isChecked(),
                    settings.exm_check.isChecked(),
                    settings.interval_edit.value(),
                    test=test
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


    timeout = TimerTimout()

    scan_now = QAction()
    scan_now.setText("Run test scan")
    scan_now.triggered.connect(lambda: timeout.onTimeout(test=True))
    menu.addAction(scan_now)

    quit = QAction()
    quit.triggered.connect(app.exit)
    quit.setText("Quit")
    menu.addAction(quit)

    tray.show()

    timer = QTimer()
    timer.timeout.connect(timeout.onTimeout)
    timer.start(1000)

    sys.exit(app.exec())

