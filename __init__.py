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
        global is_le_working
        if is_le_working == 1:
            self.add_event('speak', self.sendMessageToMindX)
            self.add_event('le-restaurant-skill:response',
                           self.responseHandler)

    @intent_handler('restaurant.le.intent')
    def handle_mindx_query(self):
        global is_le_working
        if is_le_working == 0:
            is_le_working = 1
            msg = "Le Restaurant skill is now active."
            logger.info(msg)

    def sendMessageToMindX(self, message):
        query = message.data.get("utterance")
        data = {"query": query}
        if headers["X-Conversation-Id"] is None:
            headers["X-Conversation-Id"] = conversation_id
        if query != "":
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            template = response_data['data']['channel-result'][0]['channel-message']['template']
            conversation_id = response_data['data']['conversation_id']
            msg = update.message.template
            logger.info("Le-restaurant-Message from MindX: " + msg)
            self.bus.emit(Message('recognizer_loop:utterance', {"utterances": [
                msg], "lang": self.lang}))  # , "session": session_id}))
            query = ""
            
    def responseHandler(self, message):
        response = message.data.get("utterance")
        self.bus.emit(Message("le-restaurant-skill:response",
                      {"intent_name": "le-restaurant-response", "utterance": response}))

    def shutdown(self):  # shutdown routine
        global is_le_working
        if is_le_working == 0:
            # shutdown skill
            super(LeRestaurant, self).shutdown()

    def stop(self):
        global is_le_working
        is_le_working = 0
        msg = "Le Restaurant skill is now inactive."
        logger.info("Le-restaurant-Message from MindX: " + msg)
        
def create_skill():
    return LeRestaurant()
