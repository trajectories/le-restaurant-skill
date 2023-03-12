from mycroft import MycroftSkill, intent_handler
import requests
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message

logger = getLogger(__name__)


class LeRestaurant(MycroftSkill):
    def __init__(self):
        super(LeRestaurant, self).__init__(name="LeRestaurant")
        self.is_le_working = 0
        self.skill_id = 'le-restaurant-skill'

    def initialize(self):
        self.url = self.settings.get("url")
        self.api_key = self.settings.get("api_key")
        if self.is_le_working == 1:
            self.add_event('le-restaurant-skill:response',
                           self.sendMessage)
            self.add_event('speak', self.responseMessage)

    @intent_handler('restaurant.le.intent')
    def start_le_restaurant_skill(self):
        if self.is_le_working == 0:
            self.is_le_working = 1
            msg = "Le Restaurant skill is now active."
            logger.info(msg)

    def sendMessage(self, message):
        if self.is_le_working == 1:
            query = message.data.get("utterance")
            data = {"query": query}
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer "+self.api_key,
                "X-Conversation-Id": self.conversation_id
            }
            if headers["X-Conversation-Id"] == "":
                headers["X-Conversation-Id"] = self.conversation_id
            response = requests.post(self.url, headers=headers, json=data)

    def responseMessage(self, message):
        response_data = response.json()
        template = response_data['data']['channel-result'][0]['channel-message']['template']
        self.conversation_id = response_data['data']['conversation_id']
        template = message.data.get("utterance")
        self.bus.emit(Message("le-restaurant-skill:response",
                      {"intent_name": "le-restaurant-response", "utterance": template, "skill_id": self.skill_id}))

    # def check_for_shutdown(self):
    #     if self.is_le_working == 0:
    #         self.remove_event('recognizer_loop:utterance',
    #                        self.sendMessage)
    #         self.stop()
    #     else:
    #         self.sendMessage(self, message)

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
