#!/usr/bin/python3 -OO
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
import json
import traceback
from os.path import basename
from irc.bot import ServerSpec, SingleServerIRCBot
from handler import BotHandler


class IrcBot(SingleServerIRCBot):
    def __init__(self, nick, host, nickpass, port=6667):
        """Setup everything.
        """
        serverinfo = ServerSpec(host, port, nickpass)
        SingleServerIRCBot.__init__(self, [serverinfo], nick, nick)
        #fix unicode problems
        self.connection.buffer_class.errors = 'replace'

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
        try:
            self.handler.handle(info)
        except Exception as ex:
            trace = traceback.extract_tb(ex.__traceback__)
            logging.error(trace)
            trace = trace[-1]
            trace = [basename(trace[0]), trace[1]]
            name = type(ex).__name__
            c.privmsg(channel, '%s in %s on line %s: %s' % (name, trace[0], trace[1], str(ex)))

    def on_welcome(self, c, e):
        logging.info("Connected to server.")
        self.handler = BotHandler(c)
        for i in json.load(open("channels.json"))["autojoin"]:
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
    conf = json.load(open("config.json"))
    bot = IrcBot(conf["nick"], conf["host"], conf["nickpass"])
    bot.start()

if __name__ == "__main__":
    main()
