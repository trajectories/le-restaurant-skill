from mycroft import MycroftSkill, intent_handler
import requests
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message

logger = getLogger(__name__)


class LeRestaurant(MycroftSkill):
    def __init__(self):
        super(LeRestaurant, self).__init__(name="LeRestaurant")
        self.is_le_working = 0
        self.url = ""
        self.api_key = ""
        self.conversation_id = ""
        
    def initialize(self):
        self.url = self.setting.get("url")
        self.api_key = self.setting.get("api_key")
        global is_le_working
        if is_le_working == 1:
            self.add_event('recognizer_loop:utterance',
                           self.sendMessageToMindX)

    @intent_handler('restaurant.le.intent')
    def start_le_restaurant_skill(self):
        if self.is_le_working == 0:
            self.is_le_working = 1
            msg = "Le Restaurant skill is now active."
            logger.info(msg)

    def sendMessageToMindX(self, message):
        self.url = self.setting.get("url")
        self.api_key = self.setting.get("api_key")
        global is_le_working
        while is_le_working == 1:
            query = message.data.get("utterance")
            data = {"query": query}
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer "+self.api_key,
            }
            if headers["X-Conversation-Id"] is None:
                headers["X-Conversation-Id"] = self.conversation_id
            if query != "":
                response = requests.post(self.url, headers=headers, json=data)
                response_data = response.json()
                template = response_data['data']['channel-result'][0]['channel-message']['template']
                self.conversation_id = response_data['data']['conversation_id']
                self.bus.emit(Message("le-restaurant-skill:response",
                        {"intent_name": "le-restaurant-response", "utterance": template}))
                query = ""
            
    def shutdown(self):  # shutdown routine
        if self.is_le_working == 0:
            # shutdown skill
            super(LeRestaurant, self).shutdown()

    def stop(self):
        self.is_le_working = 0
        msg = "Le Restaurant skill is now inactive."
        logger.info("Le-restaurant-Message from MindX: " + msg)


def create_skill():
    return LeRestaurant()