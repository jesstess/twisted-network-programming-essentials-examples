import sys

from twisted.python.log import FileLogObserver

class ColorizedLogObserver(FileLogObserver):
    def emit(self, eventDict):
        # Reset text color.
        self.write("\033[0m")

        if eventDict["isError"]:
            # ANSI escape sequence to color text red.
            self.write("\033[91m")

        FileLogObserver.emit(self, eventDict)

def logger():
    return ColorizedLogObserver(sys.stdout).emit
