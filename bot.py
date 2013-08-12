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
import json
class IrcBot(SingleServerIRCBot):
    def __init__(self, nick, host, nickpass, port=6667):
        """Setup everything.
        """
        serverinfo = ServerSpec(host, port, nickpass)
        SingleServerIRCBot.__init__(self, [serverinfo], nick, nick)
        
    def handle_msg(self, msgtype, c, e):
        if msgtype != 'nick':
            msg = " ".join(e.arguments)
        else:
            msg = e.target
        nick = e.source.nick
        if e.target[0] == '#':
            channel = e.target
        else:
            channel = "private"
        info = {'type': msgtype, 'data': msg, 'sender': nick, 
                'channel': channel, 
                'hostmask': "%s!%s" % (nick, e.source.userhost)}
        self.handler.handle(info)

    def on_welcome(self, c, e):
        logging.info("Connected to server.")
        self.handler = BotHandler(c)
        for i in json.loads(open("channels.json").read())["autojoin"]:
            c.join(i)
            logging.info("Joined channel %s." % i)

    def on_pubmsg(self, c, e):
        self.handle_msg('message', c, e)

    def on_privmsg(self, c, e):
        self.handle_msg('message', c, e)

    def on_join(self, c, e):
        self.handle_msg('join', c, e)

    def on_part(self, c, e):
        self.handle_msg('part', c, e)

    def on_kick(self, c, e):
        self.handle_msg('kick', c, e)

    def on_mode(self, c, e):
        self.handle_msg('mode', c, e)

    def on_nick(self, c, e):
        self.handle_msg('nick', c, e)

    def get_version(self):
        return "IPTTBot -- https://github.com/Vacation9/iptt -- developed by Fox Wilson and Samuel Damashek"

def main():
    logging.basicConfig(level=logging.DEBUG)
    conf = json.loads(open("config.json").read())
    bot = IrcBot(conf["nick"], conf["host"], conf["nickpass"])
    bot.start()

if __name__ == "__main__":
    main()
