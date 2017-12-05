# With love from Johannes
# Python2 compatible version


from Tkinter import Tk
import tkFileDialog as filedialog
import os


def ask_open_directory():
    """
    Opens a window to select an input/output directory.
    :returns a directory path
    """

    # Instantiate Tk
    root = Tk()

    # Hide main window
    root.withdraw()

    # Set focus on the window. This only works on MacOS
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    # Open selector
    dirpath = filedialog.askdirectory()

    # Update to make sure that the file selector closes afterwards
    root.update()

    return dirpath



def ask_open_filenames(return_path = False):
    """
    Opens a window to select one or more input/output files.
    :param return_path:  returns the path of the first instead filename
    :returns a list of files selected with paths
    """

    # Instantiate Tk interface
    root = Tk()

    # Prevent an actual interface from showing. We just want the file selection window
    root.withdraw()

    # Set focus on the window. This only works on MacOS
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

    # Open filename selector
    filelist = filedialog.askopenfilenames()

    # Grab path from the first file selected (they're all in the same directory anyway)
    dirpath = os.path.dirname(filelist[0])

    # Avoids multiple return statements in one function
    return dirpath if return_path else filelist