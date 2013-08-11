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

class BotHandler:
    def __init__(self, connection):
        self.connection = connection
        
    def handle(self, opts):
        mtype = opts['type']
        mdata = opts['data']
        msender = opts['sender']
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
            if mchannel == 'private':
                pass
            else:
                pass
        elif mtype == 'action':
            if mchannel == 'private':
                pass
            else:
                pass
        elif mtype == 'join':
            pass
        elif mtype == 'part':
            pass
        elif mtype == 'quit':
            pass
        elif mtype == 'kick':
            pass
        
        
        
