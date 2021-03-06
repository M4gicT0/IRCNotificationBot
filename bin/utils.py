#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 transpalette <transpalette@arch-cactus>
#
# Distributed under terms of the MIT license.

"""
Utility class
"""

import json
import subprocess

from pathlib import Path

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Util(metaclass = Singleton):
    config_locations = [
        str(Path.cwd()) + "/debug.config.json", # Debug config
        str(Path.home()) + "/.config/IRCNotificationBot/config.json" # Prod config
    ]

    debug_conf = {}
    conf = {}

    configLoaded = False


    def loadConfig(self, debug):
        if debug: print("[DEBUG] Loading debug config...")
        else: print("[INFO] Loading production config...")

        if debug:
            config_location = self.config_locations[0]
        else:
            config_location = self.config_locations[1]

        with open(config_location) as config_file:
            config_entries = json.load(config_file)

        for key in config_entries:
            value = config_entries[key]
            if key == 'notifications':
                if debug:
                    value['join']['body'] = value['join']['body'].replace('##CHANNEL##', self.debug_conf['channel'])
                    value['part']['body'] = value['part']['body'].replace('##CHANNEL##', self.debug_conf['channel'])
                else:
                    value['join']['body'] = value['join']['body'].replace('##CHANNEL##', self.conf['channel'])
                    value['part']['body'] = value['part']['body'].replace('##CHANNEL##', self.conf['channel'])
            
            if debug:
                self.debug_conf[key] = value
            else:
                self.conf[key] = value

        self.configLoaded = True

    @staticmethod
    def notify(title, body):
        subprocess.call(["/usr/bin/notify-send", title, body, "-t", "10000", "--icon=" + str(Path.cwd()) + "/img/irc_logo.png"])


    @staticmethod
    def config(key, debug = False):
        sUtil = Util() # Call the Singleton instantiation
        if not sUtil.configLoaded:
            sUtil.loadConfig(debug)

        if debug:
            return sUtil.debug_conf[key]
        else:
            return sUtil.conf[key]
        
