from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from zeroconf import ServiceBrowser, Zeroconf
import urllib.request

roomba_list = []

class MyListener:
    def remove_service(self, zeroconf, type, name):
        roomba_list.remove(name.split('.')[0])
    def add_service(self, zeroconf, type, name):
        roomba_list.append(name.split('.')[0])

class RoombaSerialCommand(MycroftSkill):

    def __init__(self):
        MycroftSkill.__init__(self)
        zeroconf = Zeroconf()
        listener = MyListener()
        browser = ServiceBrowser(zeroconf, '_roomba._tcp.local.', listener)

    @intent_handler(IntentBuilder('ListRoomba').require('List').require('Roomba'))
    def handle_list_roomba(self, message):
        if roomba_list:
            self.speak( ', '.join(map(str, roomba_list)) )
        else:
            self.speak_dialog('no.roomba')

    @intent_handler(IntentBuilder('TellRoombaTo').require('Tell').require('Roomba').require('ToCommand'))
    def handle_tell_roomba_to(self, message):
        if roomba_list: # TODO, multiple roombas
            try:
                roomba_command_url = 'http://%s/do/%s/' % ( roomba_list[0], message.data.get('ToCommand') )
                response = urllib.request.urlopen(roomba_command_url)
                roomba_response = response.read().decode('utf-8')
                self.speak_dialog('roomba.responds', data={'roomba_response':roomba_response})
            except:
                # Roomba not hittable. Remove it from the list.
                roomba_list.remove(roomba_list[0])
                self.speak_dialog('no.roomba')
        else:
            self.speak_dialog('no.roomba')

def create_skill():
    return RoombaSerialCommand()

