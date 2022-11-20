"""Module to save and load data from json file"""
import json


class Database:
    """ Class to save and load data from json file

    Methods:
         save(data): Save passed data to json file
         load(): Load data from json file
    """
    def __init__(self, filename, mode='r'):
        """ Database class constructor"""
        self.file = None
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        """ Implemented to use as context manager"""
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Implemented to use as context manager"""
        self.file.close()

    def save(self, data: list):
        """ Save passed data to json file

        Args:
            data (list): with data to save

        """
        json.dump(data, self.file)

    def load(self):
        """ Load data from json file

        Returns: data from json file

        """
        return json.load(self.file)
