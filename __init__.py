from mycroft import MycroftSkill, intent_handler
import requests
import json
from mycroft.util.log import getLogger
from alsaaudio import Mixer
from mycroft.util.log import LOG
from mycroft.api import DeviceApi
from mycroft.audio import wait_while_speaking
from mycroft.messagebus.message import Message

logger = getLogger(__name__)

url = "https://mindx.mind.ai/api/v1/gateway/default/u0W0dvyUR9K_pUX5-bEZlg/2ILfgsKlSHi7bcFDc8DPnQ"
api_key = 'kq2kYszSQGesoMhXZfmpXA'
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+api_key,
}

speak_le = 0
loaded = 0
audioinit = 0
is_le_working = 0


class LeRestaurant(MycroftSkill):
    def __init__(self):
        super(LeRestaurant, self).__init__(name="LeRestaurant")

    def initialize(self):
        # Handling settings changes
        global is_le_working
        if is_le_working == 1:
            self.settings_change_callback = self.on_settings_changed
            self.on_settings_changed()
            self.add_event('le-restaurant-skill:response', self.sendMessageToMindX)
            self.add_event('speak', self.responseHandler)

            # Connection to MindX API
            try:
                pass
            except:
                pass

            global loaded  # get global variable
            if loaded == 0:  # check if bot has just started
                loaded = 1  # make sure that users gets this message only once bot is newly loaded
                if self.mute == "false":
                    msg = "Le Restaurant Skill is loaded"
                    self.sendMycroftSay(msg)
                loadedmessage = "Le Restaurant Skill on Mycroft Unit \"" + self.UnitName + \
                    "\" is loaded and ready to use!"  # give User a nice message
                try:
                    # send welcome message to user 1
                    wbot.send_message(chat_id=self.user_id1,
                                      text=loadedmessage)
                except:
                    pass
                try:
                    # send welcome message to user 2
                    wbot.send_message(chat_id=self.user_id2,
                                      text=loadedmessage)
                except:
                    pass

    def on_settings_changed(self):
        global speak_le
        speak_le = 0
        self.mute = str(self.settings.get('MuteIt', ''))
        if (self.mute == 'True') or (self.mute == 'true'):
            try:
                self.mixer = Mixer()
                msg = "Le Restaurant Messages will temporary mute Mycroft"
                logger.info(msg)
            except:
                global audioinit
                if audioinit == 0:
                    audioinit = 1
                    msg = "There is a problem with alsa audio, mute is not working!"
                    self.sendMycroftSay(msg)
                    logger.info(
                        "There is a problem with alsaaudio, mute is not working!")
                self.mute = 'false'
        else:
            logger.info("Telegram: Muting is off")
            self.mute = "false"

        try:
            # Get Bot Token from settings.json
            self.UnitName = DeviceApi().get()['name']
            MyCroftDevice = self.settings.get('Device')
        except:
            pass

        try:
            # self.bottoken = ""
            if MyCroftDevice == self.UnitName:
                logger.debug("Found MyCroft : " + self.UnitName)
            #    self.bottoken = self.settings.get('TeleToken1', '')
            else:
                msg = (
                    "No or incorrect Device Name specified! Your DeviceName is: " + self.UnitName)
                logger.info(msg)
                self.sendMycroftSay(msg)
        except:
            pass

    @intent_handler('restaurant.le.intent')
    def handle_mindx_query(self):
        global is_le_working
        if is_le_working == 0:
            is_le_working = 1
            msg = "Le Restaurant skill is now active."
            logger.info(msg)

    def sendMycroftUtt(self, msg):
        self.bus.emit(Message('recognizer_loop:utterance', {"utterances": [
                      msg], "lang": self.lang}))  # , "session": session_id}))

    def sendMycroftSay(self, msg):
        self.bus.emit(Message('speak', {"utterance": msg, "lang": self.lang}))

    def sendMessageToMindX(self, message):
        query = message.data.get("utterance")
        data = {"query": query}
        if headers["X-Conversation-Id"] is None:
            headers["X-Conversation-Id"] = conversation_id
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        template = response_data['data']['channel-result'][0]['channel-message']['template']
        conversation_id = response_data['data']['conversation_id']
        msg = update.message.template
        global speak_le
        speak_le = 1
        logger.info("Le-restaurant-Message from User: " + msg)
        self.add_event('recognizer_loop:audio_output_start', self.muteHandler)
        self.sendMycroftUtt(msg)

    def responseHandler(self, message):
        global speak_le
        if speak_le == 1:
            speak_le = 0
            response = message.data.get("utterance")
            self.bus.emit(Message("le-restaurant-skill:response",
                          {"intent_name": "le-restaurant-response", "utterance": response}))

    def muteHandler(self, message):
        global speak_le
        if (self.mute == 'true') or (self.mute == 'True'):
            self.mixer.setmute(1)
            wait_while_speaking()
            self.mixer.setmute(0)
        self.remove_event('recognizer_loop:audio_output_start')

    def shutdown(self):  # shutdown routine
        global speak_le
        speak_le = 0
        # shutdown skill
        super(LeRestaurant, self).shutdown()

    def stop(self):
        global speak_le
        speak_le = 0


def create_skill():
    return LeRestaurant()
