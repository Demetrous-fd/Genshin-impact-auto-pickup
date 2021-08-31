# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QMainWindow, QWidget, QKeySequenceEdit, QFormLayout, QLabel, QComboBox, QHBoxLayout, \
    QPushButton, QLineEdit
from PySide2.QtCore import QSize, QRect, QThread, Slot, Signal, QMetaObject, QCoreApplication
from PySide2.QtGui import Qt

from config import update_config, read_config, default_config
from captureloop import QCaptureLoop, Model
from ScanKeys import Key


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        self.__show_capture = kwargs["show_capture"]
        kwargs.pop("show_capture")

        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("GIAP")
        self.resize(272, 164)
        self.setMinimumSize(QSize(272, 164))
        self.setMaximumSize(QSize(272, 164))

        widget = Widget(self)
        self.setCentralWidget(widget.setupUi())
        self.statusBar().showMessage("Waiting for the capture of the game")

        self.loop = QThread()
        config = read_config()
        model = Model(dnn_target=config["Target"])
        self.captureLoop = QCaptureLoop(None, model, config,
                                        show_capture=self.__show_capture)
        self.captureLoop.moveToThread(self.loop)

        self.captureLoop.sendEvent.connect(self.setStatusBarText)
        widget.updateEvent.connect(self.captureLoop.updateHandler)
        widget.switchEvent.connect(self.captureLoop.switchHandler)
        widget.switchEvent.connect(self.switchHandler)
        self.loop.started.connect(self.captureLoop.run)
        self.loop.start()
        self.show()

    @Slot()
    def setStatusBarText(self, text):
        self.statusBar().showMessage(text)

    def closeEvent(self, event):
        self.captureLoop.stop()
        self.loop.quit()
        self.loop.wait()
        event.accept()

    @Slot()
    def switchHandler(self, data):
        print(data)
        if data == "Enable":
            self.setStatusBarText("Auto pickup enable")
        else:
            self.setStatusBarText("Auto pickup disable")


class Widget(QWidget):
    updateEvent = Signal(object)
    switchEvent = Signal(object)

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"MainWindow")
        self.setWindowModality(Qt.NonModal)
        self.resize(272, 160)
        self.setMinimumSize(QSize(272, 160))
        self.setMaximumSize(QSize(272, 160))
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(11, 13, 246, 105))
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBox_Target = QComboBox(self.widget)
        self.comboBox_Target.addItem("")
        self.comboBox_Target.addItem("")
        self.comboBox_Target.addItem("")
        self.comboBox_Target.setObjectName(u"comboBox_Target")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox_Target)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.comboBox_FPS = QComboBox(self.widget)
        self.comboBox_FPS.addItem("")
        self.comboBox_FPS.addItem("")
        self.comboBox_FPS.addItem("")
        self.comboBox_FPS.addItem("")
        self.comboBox_FPS.setObjectName(u"comboBox_FPS")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox_FPS)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.comboBox_clickRate = QComboBox(self.widget)
        self.comboBox_clickRate.addItem("")
        self.comboBox_clickRate.addItem("")
        self.comboBox_clickRate.addItem("")
        self.comboBox_clickRate.setObjectName(u"comboBox_clickRate")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_clickRate)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_4)

        self.keyEdit = KeyEdit(self.widget)
        self.keyEdit.setObjectName(u"keyEdit")

        self.horizontalLayout.addWidget(self.keyEdit)

        self.pushButton_default = QPushButton(self.widget)
        self.pushButton_default.setObjectName(u"btn_default")

        self.horizontalLayout.addWidget(self.pushButton_default)

        self.formLayout.setLayout(3, QFormLayout.SpanningRole, self.horizontalLayout)

        self.pushButton_switch = QPushButton(self.centralwidget)
        self.pushButton_switch.setObjectName(u"btn_switch")
        self.pushButton_switch.setGeometry(QRect(8, 118, 249, 23))

        QWidget.setTabOrder(self.comboBox_Target, self.comboBox_FPS)
        QWidget.setTabOrder(self.comboBox_FPS, self.comboBox_clickRate)

        self.retranslateUi(self)
        self.connection()
        self.loadConfig()

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        self.label.setText(QCoreApplication.translate("MainWindow", u"Target:", None))
        self.comboBox_Target.setItemText(0, QCoreApplication.translate("MainWindow", u"CPU", None))
        self.comboBox_Target.setItemText(1, QCoreApplication.translate("MainWindow", u"OpenCL", None))
        self.comboBox_Target.setItemText(2, QCoreApplication.translate("MainWindow", u"CUDA", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Frame rate:", None))
        self.comboBox_FPS.setItemText(0, QCoreApplication.translate("MainWindow", u"15", None))
        self.comboBox_FPS.setItemText(1, QCoreApplication.translate("MainWindow", u"10", None))
        self.comboBox_FPS.setItemText(2, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_FPS.setItemText(3, QCoreApplication.translate("MainWindow", u"Unlimeted", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Click rate:", None))
        self.comboBox_clickRate.setItemText(0, QCoreApplication.translate("MainWindow", u"Normal", None))
        self.comboBox_clickRate.setItemText(1, QCoreApplication.translate("MainWindow", u"Fast", None))
        self.comboBox_clickRate.setItemText(2, QCoreApplication.translate("MainWindow", u"Ultra fast", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Key:", None))
        self.pushButton_default.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.pushButton_switch.setText(QCoreApplication.translate("MainWindow", u"Disable", None))

    def connection(self):
        self.comboBox_Target.currentTextChanged.connect(lambda: self.changeValue(self.comboBox_Target))
        self.comboBox_clickRate.currentTextChanged.connect(lambda: self.changeValue(self.comboBox_clickRate))
        self.comboBox_FPS.currentTextChanged.connect(lambda: self.changeValue(self.comboBox_FPS))

        self.keyEdit.editingFinished.connect(lambda: self.on_editingFinished())
        self.pushButton_default.clicked.connect(self.default)
        self.pushButton_switch.clicked.connect(self.switch)

        self.updateEvent.connect(Slot())
        self.switchEvent.connect(Slot())

    def loadConfig(self):
        config = read_config()
        self.comboBox_Target.setCurrentText(config["Target"])
        self.comboBox_clickRate.setCurrentText(config["Click rate"])
        self.comboBox_FPS.setCurrentText(str(config["FPS"]))
        self.keyEdit.setKey(config["Key"])

    @Slot()
    def on_editingFinished(self):
        print(self.keyEdit.last_key)
        self.changeValue(self.keyEdit)

    @Slot()
    def switch(self):
        if self.pushButton_switch.text() == "Disable":
            self.pushButton_switch.setText("Enable")
            self.switchEvent.emit("Disable")
        else:
            self.pushButton_switch.setText("Disable")
            self.switchEvent.emit("Enable")

    @Slot()
    def default(self):
        default_config()
        self.loadConfig()
        print(f"Set default config")

    @Slot()
    def changeValue(self, sender):
        data = []

        if isinstance(sender, QComboBox):
            text = sender.currentText().strip()

            if sender.objectName() == "comboBox_Target":
                print("Target: ", text)
                update_config("Target", text)
                data = ["Target", text]

            elif sender.objectName() == "comboBox_FPS":
                print("FPS: ", text)
                fps = int(text) if text != "Unlimeted" else 0
                update_config("FPS", fps)
                data = ["FPS", fps]

            else:
                print("Click rate: ", text)
                update_config("Click rate", text)
                data = ["Click rate", text]

        elif isinstance(sender, KeyEdit):
            key = self.keyEdit.last_key.scancode
            update_config("Key", key)
            data = ["Key", key]

        self.updateEvent.emit(data)


class KeyEdit(QKeySequenceEdit):
    def __init__(self, *args, **kwargs):
        super(KeyEdit, self).__init__(*args, **kwargs)
        self.__line_edit = self.findChild(QLineEdit, "qt_keysequenceedit_lineedit")
        self.__line_edit.setAlignment(Qt.AlignCenter)
        self.last_key = Key("F")
        self.__default_key = Key("F")

        self.__line_edit.setText(self.last_key.key)
        self.clearFocus()

    def keyPressEvent(self, event):
        if event.nativeScanCode() in (1, 15, 28, 29, 42, 54, 56, 57, 58, 69, 284, 285, 312, 325, 347):
            self.__line_edit.setText(self.last_key.key)
            self.clearFocus()

        else:
            try:
                self.last_key = Key(event.nativeScanCode())
            finally:
                self.__line_edit.setText(self.last_key.key)
                self.editingFinished.emit()

    def setKey(self, key):
        self.last_key = Key(key)
        self.__line_edit.setText(self.last_key.key)
        self.editingFinished.emit()

    def default(self):
        self.last_key = self.__default_key
        self.__line_edit.setText(self.last_key.key)
        self.editingFinished.emit()
