"""
This module by default contains some helper functions which
are common to both dbOperations and fileOperations. It also contains
certain methods which require frequent user
"""

import errno
import os

def getExtensionOfFile(filename):
    """
        Returns extension of a file in string format

        Args:
            filename(str): name of the file
        Returns:
            str: extension of file
    """
    return filename.rsplit('.', 1)[1]

def mkdir_p(path):
    """
        implements mkdir -p functinality of linux shell in python. It might raise
        error in concurrent conditions
    """
    if not os.path.exists(path):
        os.makedirs(path)
