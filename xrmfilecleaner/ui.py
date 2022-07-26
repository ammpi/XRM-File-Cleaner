from xrmfilecleaner.qt import *
import xrmfilecleaner
from xrmfilecleaner.help import get_resource


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.conf = QSettings()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.form = QFormLayout(self)
        self.layout.addLayout(self.form)

        self.interval_edit = QSpinBox(self)
        self.interval_edit.setMinimum(1)
        self.interval_edit.setMaximum(99)
        self.addRow(self.interval_edit, "Days offset:", "interval_days", 30)

        self.scan_time = QTimeEdit(self)
        self.addRow(self.scan_time, "Scan time:", "scan_time", QTime(0, 0, 0))

        self.exm_ooc_check = QCheckBox(self)
        self.addRow(self.exm_ooc_check, "Delete .txm-exm-ooc files", "del_ooc", True)

        self.exm_check = QCheckBox(self)
        self.addRow(self.exm_check, "Delete .txm-exm files", "del_exm", True)

        self.dirs_list = QTextEdit(self)
        self.addRow(self.dirs_list, "Directories:", "dirs", "")

    def addRow(self, widget: QWidget, name: str, conf_par: str, default):
        val = self.conf.value(conf_par)
        if val is None:
            val = default

        if isinstance(widget, QSpinBox):
            widget.setValue(val)
            widget.valueChanged.connect(lambda x: self.conf.setValue(conf_par, x))
        elif isinstance(widget, QTimeEdit):
            widget.setTime(val)
            widget.timeChanged.connect(lambda x: self.conf.setValue(conf_par, x))
        elif isinstance(widget, QCheckBox):
            widget.setChecked(val)
            widget.stateChanged.connect(lambda x: self.conf.setValue(conf_par, x))
        elif isinstance(widget, QTextEdit):
            widget.setText(val)
            widget.textChanged.connect(lambda: self.conf.setValue(conf_par, widget.toPlainText()))
        else:
            raise ValueError("Don't know what to do with the given type")

        self.form.addRow(name, widget)


class StatusWidget(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setIcon(get_resource("icon.png"))

