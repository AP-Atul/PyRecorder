import os.path
import sys

from PyQt5 import QtGui
from PyQt5.Qt import *
from joblib import dump, load

from controller import Controller

dark = True

"""
Pro tip: Use Ctrl + D to change the theme ;)
"""


class App(QWidget):
    """
    Initial class to create an UI with several components like layouts, labels, buttons, etc
    """
    def __init__(self):
        global dark
        super().__init__()

        if os.path.isfile('settings.prop'):
            dark = load('settings.prop')

        self.setGeometry(50, 50, 450, 150)
        self.setMinimumHeight(150)
        self.setMinimumWidth(450)
        self.setWindowTitle('PyRecorder FFmpeg')
        self.setWindowIcon(QtGui.QIcon('icons/logo.png'))
        self.show()

        self.controller = Controller()

        self.filePath = QLineEdit()
        self.filePath.setText("/home/atul/")

        theme = QAction(QIcon('icons/dark_mode.png'), 'Change Theme', self)
        theme.setShortcut('Ctrl+D')
        theme.triggered.connect(self.changeTheme)
        self.addAction(theme)

        self.greenPalette = QPalette()
        self.greenPalette.setColor(QPalette.Button, QColor(12, 109, 26))

        self.redPalette = QPalette()
        self.redPalette.setColor(QPalette.Button, QColor(139, 0, 0))

        if dark:
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            self.setPalette(palette)
        self.initUI()

    def initUI(self):
        # ************* ALL THE LAYOUTS ************** #
        # main layout (vertical)
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)

        # bottom close button layout
        closeButtonLayout = QHBoxLayout()
        closeButtonLayout.addStretch(1)
        closeButtonLayout.setSpacing(10)

        # ************* ALL THE WIDGETS ************** #
        # info label
        infoLabel = QLabel()
        infoLabel.setText("Enter the path and file name")
        infoLabel.setFont(QtGui.QFont('Ubuntu', 12, QtGui.QFont.Bold))
        mainLayout.addWidget(infoLabel)

        # input text box
        self.controller.output.connect(self.setMessage)
        mainLayout.addWidget(self.filePath)

        # compare button
        compareButton = QPushButton()
        compareButton.setText("Start")
        compareButton.clicked.connect(self.start)
        compareButton.setPalette(self.greenPalette)
        compareButton.update()
        closeButtonLayout.addWidget(compareButton)

        # close button
        closeButton = QPushButton()
        closeButton.setText("Stop")
        closeButton.setPalette(self.redPalette)
        closeButton.clicked.connect(self.stop)
        closeButtonLayout.addWidget(closeButton)

        # add all components to mail layout
        mainLayout.addLayout(closeButtonLayout)

        # add main layout to the window
        self.setLayout(mainLayout)

    def changeTheme(self):
        """
        Change the theme of the UI. Settings are saved in settings,prop
        `Press Ctrl + D`
        """
        dump(not dark, "settings.prop")
        self.__init__()

    def start(self):
        file = self.filePath.text()
        if len(file) > 0:
            self.controller.setOutputFile(file)
        else:
            QMessageBox.question(self, 'Message', "Please enter file name.", QMessageBox.Ok)

    def setMessage(self, msg):
        QMessageBox.question(self, 'Message', msg, QMessageBox.Ok)

    def stop(self):
        if self.controller is not None:
            self.controller.terminate()


def main():
    app = QApplication(sys.argv)
    application = App()
    application.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
