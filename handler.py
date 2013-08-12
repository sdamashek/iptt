#!/usr/bin/python
# Copyright (C) 2013 Samuel Damashek and Fox Wilson
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
import json, re

def get_commands(mtype=None):
    cmds = json.loads(open("commands.json").read())
    if mtype is None: return cmds
    newcmds = {}
    for i in cmds:
        if cmds[i]["trigger"] == mtype:
            newcmds[i] = cmds[i]
    return newcmds

def mask_in_group(mask, group):
    groups = json.loads(open("groups.json").read())
    for i in groups[group]:
        if re.match(i, mask):
            return True
    return False

def channel_in_group(channel, group):
    chans = json.loads(open("channels.json").read())
    for i in chans[group]:
        if re.match(i, channel):
            return True
    return False

class BotHandler:
    def __init__(self, connection):
        self.connection = connection
    
    def handle(self, opts):
        mtype = opts['type']
        mdata = opts['data']
        msender = opts['sender']
        mhostmask = opts['hostmask']
        if 'channel' in opts:
            mchannel = opts['channel']
        else:
            mchannel = 'private'
        # long branchy thingy
        if mtype == 'mode':
            pass
        elif mtype == 'nick':
            pass
        elif mtype == 'message':
            self.handle_message(mdata, mchannel, msender, mhostmask)
        elif mtype == 'action':
            if mchannel == 'private':
                pass
            else:
                pass
        elif mtype == 'join':
            self.handle_join(mdata, mchannel, msender, mhostmask)
        elif mtype == 'part':
            self.handle_part(mdata, mchannel, msender, mhostmask)
        elif mtype == 'quit':
            pass
        elif mtype == 'kick':
            pass

    def do_eligible(self, cmd, data, channel, sender, hostmask):
        targs = cmd["triggerargs"]
        x = re.match(targs["data"], data)
        if x:
            if channel_in_group(channel, cmd["triggerargs"]["changroup"]):
                if mask_in_group(hostmask, cmd["triggerargs"]["nickgroup"]):
                    self.do_thing(cmd["result"], {"channel": channel,
                        "sender": sender}, x)

    def handle_message(self, data, channel, sender, hostmask):
        cmds = get_commands('message')
        for i in cmds:
            self.do_eligible(cmds[i], data, channel, sender, hostmask)

    def handle_join(self, data, channel, sender, hostmask):
        cmds = get_commands('join')
        for i in cmds:
            self.do_eligible(cmds[i], data, channel, sender, hostmask)

    def handle_part(self, data, channel, sender, hostmask):
        cmds = get_commands('part')
        for i in cmds:
            self.do_eligible(cmds[i], data, channel, sender, hostmask)

    def do_rep(self, match, data, string):
        try:
            string = string.replace("{sender}", data["sender"])
            string = string.replace("{chan}", data["channel"])
            string = string.replace("{g1}", match.group(1))
            string = string.replace("{g2}", match.group(2))
            string = string.replace("{g3}", match.group(3))
            string = string.replace("{g4}", match.group(4))
            string = string.replace("{g5}", match.group(5))
            string = string.replace("{g6}", match.group(6))
            string = string.replace("{g7}", match.group(7))
            string = string.replace("{g8}", match.group(8))
            string = string.replace("{g9}", match.group(9))
        finally:
            return string

    def do_thing(self, thing, data, trigger):
        rtype = thing["type"]
        channel = data["channel"]
        sender = data["sender"]
        if rtype == "nothing": return
        # Message
        if rtype == "message":
            if thing["to"] == "REPLY":
                if channel == "private":
                    cto = sender
                else:
                    cto = channel
            else:
                cto = self.do_rep(trigger, data, thing["to"])
            message = self.do_rep(trigger, data, thing["content"])
            self.connection.send_raw("PRIVMSG %s :%s" % (cto, message))
        # Nick
        if rtype == "nick":
            self.connection.send_raw("NICK %s" % self.do_rep(trigger, data, thing["newnick"]))
        # Join
        if rtype == "join":
            thing["chan"] = self.do_rep(trigger, data, thing["chan"])
            if thing["chan"][0] != '#': thing["chan"] = "#%s" % thing["chan"]
            thing["chan"] = thing["chan"].split(",")[0]
            self.connection.send_raw("JOIN %s" % thing["chan"])
        # Part
        if rtype == "part":
            thing["chan"] = self.do_rep(trigger, data, thing["chan"])
            if thing["chan"][0] != '#': thing["chan"] = "#%s" % thing["chan"]
            thing["chan"] = thing["chan"].split(",")[0]
            self.connection.send_raw("PART %s" % thing["chan"])
        # Mode
        if rtype == "mode":
            thing["mode"] = self.do_rep(trigger, data, thing["mode"])
            thing["chan"] = self.do_rep(trigger, data, thing["chan"])
            self.connection.send_raw("MODE %s %s" % (thing["chan"], thing["mode"]))
        # Kick
        if rtype == "kick":
            thing["nick"] = self.do_rep(trigger, data, thing["nick"])
            thing["chan"] = self.do_rep(trigger, data, thing["chan"])
            self.connection.send_raw("KICK %s %s" % (thing["chan"], thing["nick"]))
        

