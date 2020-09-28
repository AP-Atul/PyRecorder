"""
Initiating the command line and run the command using the subprocess module
"""

import subprocess

from lib.logger import Log


class Runner:
    """
    Class to run the recording command to run the screen recorder and start recording

    Attributes
    ----------
    __outputFile : str
        name of the recording save along with path can be provided
    __run : process object
        subprocess object to run the Popen command
    """

    def __init__(self, outputFile):
        self.__outputFile = outputFile
        self.__run = None

    def buildCommand(self):
        """
        Building the final screen recording command to run by the subprocess
        The output file name is the only parameter currently

        Would add options to add fps, video formats sizes, etc

            ffmpeg -video_size 1366x768 -framerate 30 -f x11grab -i :0.0+0,0 -c:v libx264rgb -crf 0 -preset ultrafast $1

        """
        command = "ffmpeg " \
                  "-video_size 1366x768 " \
                  "-framerate 30 " \
                  "-f x11grab " \
                  "-i :0.0+0,0 " \
                  "-c:v libx264rgb " \
                  "-crf 0 " \
                  "-preset ultrafast " \
                  + str(self.__outputFile)
        return command

    def runCommand(self):
        """
        Running the command line with subprocess module, using the Log class to print some info
        and errors
        """
        self.__run = subprocess.Popen(args=self.buildCommand(),
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      shell=True,
                                      universal_newlines=True)

        for _ in iter(self.__run.stdout.readlines, ""):
            print(_)

        self.__run.stdout.close()

        if self.__run.wait():
            Log.e("Error occurred while running the PyRecorder Command line.")
            raise ChildProcessError("It's not working")

    def terminate(self):
        if self.__run is not None:
            self.__run.terminate()
        Log.i("Recording saved successfully")
