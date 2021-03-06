"""
This file implements the Config class which is used to handle resources
and configuration values
"""

from configparser import ConfigParser
import os
from os import path


class Config:
    DEFAULT_GENERAL_CONF_FILE = "resources/configuration/conf.ini"

    def __init__(self, conf_file=DEFAULT_GENERAL_CONF_FILE):
        self._conf_file = conf_file
        self._parser = ConfigParser()

    def set_file_path(self, file_path):
        self._conf_file = file_path

    def create_conf_file(self):
        f = open(self._conf_file, "w+")
        f.close()

    def config_exist(self, file_path):
        return path.exists(file_path)


    def add_section(self, section):
        self._parser.read(self._conf_file)
        self._parser.add_section(section)
        self.save_config_data()

    def set_value(self, section, key, value):
        self._parser.read(self._conf_file)
        self._parser.set(section, key, value)
        self.save_config_data()

    def save_config_data(self):
        with open(self._conf_file, 'w') as configfile:
            self._parser.write(configfile)

    def get_value(self, section, key):
        self._parser.read(self._conf_file)
        return self._parser.get(section, key)

    def delete_config(self):
        os.remove(self._conf_file)



