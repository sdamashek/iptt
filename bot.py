#!/usr/bin/python
# Copyright (C) 2013 Samuel Damashek
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import logging
from sqlalchemy import *
from irc.bot import ServerSpec, SingleServerIRCBot
from os.path import basename
from json import loads, dumps
from CONFIG import CHANNEL, NICK, NICKPASS, HOST, CTRLCHAR

class IrcBot(SingleServerIRCBot):

    def __init__(self, channel, nick, nickpass, host, port=6667):
        """Setup everything.
        """
        serverinfo = ServerSpec(host, port, nickpass)
        SingleServerIRCBot.__init__(self, [serverinfo], nick, nick)
        self.engine = create_engine('sqlite:///database.db')
        self.conn = self.engine.connect()
    
    def create_tables(self):
        self.metadata = MetaData()
        self.commands = Table('users', meta, autoload=True, autoload_with=self.engine)
        
    def handle_msg(self, msgtype, c, e):
        msg = " ".join(e.arguments)
        
        
    def get_conditions(self):
        """Returns a list of functions to call with the message"""
        s = select([self.commands])
        conditions = self.conn.execute(s)
        return [(hash_condition(c.type), hash_consequence(c.consequence), dumps(c.params)) for c in conditions]

    def hash_condition(self, type):
        """Returns a function based on the type of function and command passed"""
        return {
            'kick': lambda message, params, messtype, e: messtype == 'kick' and (params['target'] == -1 or params['target'] == e.source.nick)
        }[type]
    def hash_consequence(self, type):
        """Returns a function based on the consequence passed"""
        return {
            'kick': lambda params, c: c.send_raw("KICK %s %s :%s" % ())
        }[type]
        