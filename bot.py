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
from handler import BotHandler
import logging
CHANNEL = "#iptt"
NICK = "ipttbot"
HOST = "irc.freenode.org"

class IrcBot(SingleServerIRCBot):
    def __init__(self, nick, host, port=6667):
        """Setup everything.
        """
        serverinfo = ServerSpec(host, port, "")
        SingleServerIRCBot.__init__(self, [serverinfo], nick, nick)
        
    def handle_msg(self, msgtype, c, e):
        msg = " ".join(e.arguments)
        nick = e.source.nick
        if e.target[0] == '#':
            channel = e.target
        else:
            channel = "private"
        info = {'type': msgtype, 'data': msg, 'sender': nick, 
                'channel': channel}
        logging.info(repr(info))
        self.handler.handle(info)

    def on_welcome(self, c, e):
        logging.info("Connected to server.")
        self.handler = BotHandler(c)
        c.join(CHANNEL)
        logging.info("Joined channel %s." % CHANNEL)

    def on_pubmsg(self, c, e):
        self.handle_msg('message', c, e)

    def on_privmsg(self, c, e):
        self.handle_msg('message', c, e)

    def on_action(self, c, e):
        self.handle_msg('action', c, e)

    def on_join(self, c, e):
        self.handle_msg('join', c, e)

    def on_part(self, c, e):
        self.handle_msg('part', c, e)

    def on_kick(self, c, e):
        self.handle_msg('kick', c, e)

    def on_quit(self, c, e):
        self.handle_msg('quit', c, e)

    def on_mode(self, c, e):
        self.handle_msg('mode', c, e)

def main():
    logging.basicConfig(level=logging.INFO)
    bot = IrcBot(NICK, HOST)
    bot.start()

if __name__ == "__main__":
    main()
