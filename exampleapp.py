# import the enum type for rcon events
from rcontypes import rcon_event,rcon_receive
# import json parsing to translate server messages into JSON type
import json
from helpers import send_packet
import time
#optional: add in automatic table lookup for translating PlayerID's to Player Profile + Store
# from update_cache import get_handle_cache
# player dict for this scope only, useful for packets that only have playerId
# player_dict = {}
# handle_cache = get_handle_cache(player_dict)
vices = [11, 15, 21, 9, 17, 17, 5, 8, 18, 16, 20, 16, 12, 16, 2, 18, 15, 5, 5, 5, 14, 14, 4, 11, 17, 14, 6, 9, 23, 18, 14, 13, 11, 14, 16, 15, 13, 1, 8, 15]
wave = 204
color = 65280

def handle_chat(event_id, message_string, sock):
    # if passed in event_id is a chat_message
    if event_id == rcon_event.chat_message.value:
        # parse the json
        js = json.loads(message_string)
        # if the server message is from a player
        if 'PlayerID' in js and js['PlayerID'] != '-1':
            if '!vices' == js["Message"]:
                cmd = ""
                for i in range(0, len(vices)):
                    cmd = 'setvice "{}" "{}" "{}"'.format(js['Name'], i, vices[i])
                    send_packet(sock, cmd, rcon_receive.command.value)
                    time.sleep(0.1)
                send_packet(sock, 'setlife "{}" "{}"'.format(js['Name'], 3500), rcon_receive.command.value)

def handle_player_join(event_id, message_string, sock):
    if event_id == rcon_event.player_connect.value:
        js = json.loads(message_string)
        send_packet(sock, 'rawsay "welcome to survival simulator, {}. Commands are !vices !start !restart" "{}"'.format(js['PlayerName'], color), rcon_receive.command.value)

def handle_chat_start(event_id, message_string, sock):
    if event_id == rcon_event.chat_message.value:
        # parse the json
        js = json.loads(message_string)
        # if the server message is from a player
        if 'PlayerID' in js and js['PlayerID'] != '-1':
            if "!start" == js["Message"]:
                send_packet(sock, 'setwave "{}"'.format(wave), rcon_receive.command.value)

def handle_chat_restart(event_id, message_string, sock):
    if event_id == rcon_event.chat_message.value:
        # parse the json
        js = json.loads(message_string)
        # if the server message is from a player
        if 'PlayerID' in js and js['PlayerID'] != '-1':
            if "!restart" == js["Message"]:
                send_packet(sock, 'setwave "{}"'.format(1), rcon_receive.command.value)


def handle_chat_help(event_id, message_string, sock):
    if event_id == rcon_event.chat_message.value:
        # parse the json
        js = json.loads(message_string)
        # if the server message is from a player
        if 'PlayerID' in js and js['PlayerID'] != '-1':
            if "!help" == js["Message"]:
                send_packet(sock, 'rawsay "welcome to survival simulator, {}. Commands are !vices and !start" "{}"'.format(js['Name'], color), rcon_receive.command.value)


def handle_rcon_logged_in(event_id, message_string, sock):
    if event_id == rcon_event.rcon_logged_in.value: 
        send_packet(sock, "enablemutators", rcon_receive.command.value)


example_functions  = [handle_rcon_logged_in, handle_chat, handle_chat_start, handle_chat_help, handle_player_join, handle_chat_restart] # include handle_cache if you are using it