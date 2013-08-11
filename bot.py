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
        
    def handle_msg(self, msgtype, c, e):
        msg = " ".join(e.arguments)
