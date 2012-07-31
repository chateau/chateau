#!/usr/bin/env python3

from types import FunctionType
import logging

class Bot(object):
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.plugin_instances = []
        self._nick = None
        for plugin in self.config["plugins"]:
            inst = plugin(self)
            for name, value in plugin.__dict__: # for every class attribute
                if isinstance(value, FunctionType) and hasattr(value, 'subscription'):
                    self.subscribe(types=sub.types, callback=value)
        
    def connect(self):
        if not self.connection or not self.connection.connected:
            if self.config["transport"] == "asynchat":
                from .transports import asynchat
                transport = asynchat
            self.connection = transport.Connection(self.config["address"], self.config["port"], self.config["use_ssl"], self)
            self.connection.start()
            transport.loop()
            
        return self.connection
    
    def subscribe(self, types, callback):
        self.subscriptions += {'types': types, 'callback': callback}
    
    def handle_line(self, line):
        logging.debug(line)
        if line[0] == ":": # prefix
            prefix, command, params_str = line.split(' ', 2)
            prefix_split = prefix.split('!', 1)
            if len(prefix_split) > 1: # if the prefix is a hostmask
                prefix_hostmask = prefix[1:] # Get the prefix - the colon
                prefix_nick = prefix_split[0][1:] # Get the nickname
            else:
                prefix_nick = None
            if prefix_nick == self.nick and command == "NICK": # If our NICK changed
                self._nick = params[0] # Update internal nick
        else:
            command, params_str = line.split(' ', 1)
        
        params = params_str.split(' ')

        if command == "005": # If we're being welcomed
            self._nick = params[0] # Update internal nick
        
    def send(self, *data):
        msg = ' '.join((str(i) for i in data))
        logging.debug(msg)
        self.connection.push(msg.encode('utf_8'))
    
    @property
    def nick(self):
        return self._nick
    
    @nick.setter
    def nick(self, nick):
        self.send("NICK", nick)
    
    def handle_connect(self):
        self.send("PASS", (self.config["password"] or "*"))
        self.nick = self.config["nickname"]
        mode_numeric = 0
        if 'w' in self.config["umodes"]:
            mode_numeric += 1 << 2 # Set bit 2 (rfc2812#section-3.1.3)
        if 'i' in self.config["umodes"]:
            mode_numeric += 1 << 3 # Set bit 3 (rfc2812#section-3.1.3)
        self.send("USER", self.config["username"], mode_numeric, "*", ":"+self.config["realname"])
