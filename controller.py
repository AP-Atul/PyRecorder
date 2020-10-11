import os

from PyQt5.QtCore import QThread, pyqtSignal

from lib.ffmpegRunner import Runner
from lib.logger import Log


class Controller(QThread):
    output = pyqtSignal(str)

    def __init__(self,):
        QThread.__init__(self, parent=None)
        self.__runner = None
        self.__outputFile = None

    def setOutputFile(self, outputFile):
        self.__outputFile = outputFile
        self.start()

    def run(self):
        if not self.__check():
            Log.e("Input file does not exists")
            self.__showErrorDialog("File path does not exists")
            return

        self.__runner = Runner(self.__outputFile)
        try:
            Log.i("Started recording")
            self.__runner.runCommand()
        except ChildProcessError:
            self.__showErrorDialog("Error running FFmpeg")

    def terminate(self):
        if self.__runner is not None:
            self.__runner.terminateCommand()
            self.output.emit("Recording saved.")
        else:
            self.output.emit("Recording has not yet started.")

    def __showErrorDialog(self, message):
        self.output.emit(message)

    def __check(self):
        return os.path.isdir(os.path.split(self.__outputFile)[0])
