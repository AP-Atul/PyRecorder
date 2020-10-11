"""
Initiating the command line and run the command using the subprocess module
"""
import os
import signal
import subprocess

from lib.constants import *
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
        self.__processKilled = False

    def buildCommand(self):
        """
        Building the final screen recording command to run by the subprocess
        The output file name is the only parameter currently

        Would add options to add fps, video formats sizes, etc

            ffmpeg -video_size 1366x768 -framerate 30 -f x11grab -i :0.0+0,0 -c:v libx264rgb -crf 0 -preset ultrafast $1

        """
        command = ["ffmpeg",
                   "-y",
                   "-video_size",
                   VIDEO_SIZE,
                   "-framerate",
                   FPS,
                   "-f",
                   VIDEO_FORMAT,
                   "-i",
                   ":0.0+0,0",
                   "-f",
                   AUDIO_FORMAT,
                   "-ac",
                   "2",
                   "-i",
                   AUDIO_DEVICE,
                   "-acodec",
                   AUDIO_CODEC,
                   "-vcodec",
                   VIDEO_CODEC,
                   "-strict",
                   "experimental",
                   str(self.__outputFile)]
        return command

    def runCommand(self):
        """
        Running the command line with subprocess module, using the Log class to print some info
        and errors
        """
        self.__run = subprocess.Popen(args=self.buildCommand(),
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      universal_newlines=True,
                                      preexec_fn=os.setsid)

        if not self.__processKilled:
            for _ in iter(self.__run.stdout.readlines, ""):
                pass

        self.__run.stdout.close()

        if self.__run.wait():
            Log.e("Error occurred while running the PyRecorder Command line.")
            raise ChildProcessError("It's not working")

        return

    def terminateCommand(self):
        if self.__run is not None:
            os.killpg(os.getpgid(self.__run.pid), signal.SIGTERM)
            self.__processKilled = True
        Log.i("Recording saved successfully")
