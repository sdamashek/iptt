iptt
====

If py then thon - flexible Python IRC bot

Writing trigger/result definitions
----------------------------------
Trigger/result pairs are written in json. The commands file as a whole is a JSON list. Each command is an object. Objects are structured like so:
<code>
{
    "trigger": "message|join|part|kick|mode",
    "triggerargs": {
        "data": "regexp-matching-data", // see below table for what data is
        "nickgroup": "nickgroup", // see below
        "changroup": "changroup" // see below
    },
    "result": {
        "type": "message|join|part|kick|mode",
        "type-specific-argument": "type-specific-value"
    }
}
</code>
Nick groups
-----------
Nickname groups are defined in groups.json. The groups file is an object. Each group contains zero or more nick!user@hosts (regular expressions can be used to match these).

Channel groups
--------------
Channel groups are structured similarly to nickname groups, however, the "autojoin" channel group defines a list of channels to autojoin.

Config
------
The configuration file is, not surprisingly, JSON, and defines a server, nickname, and server password.

Type-specific arguments
-----------------------
{sender} and {chan} may be used in type-specific arguments to insert the nick of the sender and the channel, respectively.

For "message":
- to = message destination (the special value REPLY can be used)
- content = message content

For "join":
- chan = channel to join

For "part":
- part = channel to part

For "kick":
- chan = channel to kick from
- nick = nickname to kick

For "mode":
- chan = channel to set mode on
- mode = mode to set


