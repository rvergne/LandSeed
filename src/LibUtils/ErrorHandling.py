#!/usr/bin/env python3

# Error exception meaning :
#   FileBadlyWrittenException : keyword missing in a file or badly written
#   PathErrorException : path error
#   DependencyException : dependency not recognize
#   WrongParameterException : script parameter error
#   TooOldPythonVersionException : Python version too old

class Error(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class FileBadlyWrittenException(Error):
    def __init__(self, file):
        super().__init__(message)

class PathErrorException(Error):
    def __init__(self, message):
        super().__init__(message)

class DependencyException(Error):
    def __init__(self, message):
        super().__init__(message)

class WrongParameterException(Error):
    def __init__(self, message):
        super().__init__(message)

class TooOldPythonVersionException(Error):
    def __init__(self, message):
        super().__init__(message)
