from mycroft import MycroftSkill, intent_handler
import requests
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message
from websocket import create_connection, WebSocket

logger = getLogger(__name__)
speak_le = 1


class LeRestaurant(MycroftSkill):
    def __init__(self):
        super(LeRestaurant, self).__init__(name="LeRestaurant")
        self.is_le_working = 0
        self.skill_id = 'le-restaurant-skill'
        self.conversation_id = ""
        self.template = ""

    @intent_handler('restaurant.le.intent')
    def start_le_restaurant_skill(self, message):
        if self.is_le_working == 0:
            self.is_le_working = 1
            self.url = self.settings.get("url")
            self.api_key = self.settings.get("api_key")
            msg = "Le Restaurant skill is now active."
            logger.info(msg)
            self.handle_conversation(self.template)

    def send_message(self, message):
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
        if response.status_code == 200:
            response_data = response.json()
            self.template = response_data['data']['channel-result'][0]['channel-message']['template']
            self.conversation_id = response_data['data']['conversation_id']
            self.sendMycroftUtt(self.template)
            self.handle_conversation(self.template)
        
    def handle_conversation(self, template):
        if self.template == "It was nice talking to you. Have a good one!":
            self.stop()
        else:
            self.add_event('recognizer_loop:utterance', self.send_message)

    def sendMycroftUtt(self, msg):
        uri = 'ws://localhost:8181/core'
        ws = create_connection(uri)
        utt = '{"context": null, "type": "recognizer_loop:utterance", "data": {"lang": "' + \
            self.lang + '", "utterances": ["' + msg + '"]}}'
        ws.send(utt)
        ws.close()

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
