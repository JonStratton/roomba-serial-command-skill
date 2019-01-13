from mycroft import MycroftSkill, intent_file_handler


class RoombaSerialCommand(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('command.serial.roomba.intent')
    def handle_command_serial_roomba(self, message):
        self.speak_dialog('command.serial.roomba')


def create_skill():
    return RoombaSerialCommand()

