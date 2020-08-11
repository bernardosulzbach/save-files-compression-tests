# Taken from O'Reilly's Python Cookbook and adapted by Bernardo Sulzbach.
#
# This file is not covered by the project's license.

import os
import os.path


class DirectorySizeError(Exception):
    pass


def get_directory_size(start):
    try:
        # Get a list of all names of files and subdirectories in directory start
        dir_list = os.listdir(start)
    except:
        # If start is a directory, we probably have permission problems
        if os.path.isdir(start):
            raise DirectorySizeError("Cannot list directory %s." % start)
        else:
            # Otherwise, just re-raise the error so that it propagates
            raise
    try:
        total = os.stat(start).st_size
    except:
        raise DirectorySizeError("Cannot stat %s." % start)
    for item in dir_list:
        path = os.path.join(start, item)
        if os.path.isdir(path):
            total += get_directory_size(path)
        else:
            try:
                total += os.stat(path).st_size
            except:
                raise DirectorySizeError("Cannot stat %s." % path)
    return total
