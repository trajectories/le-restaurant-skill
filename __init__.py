from mycroft import MycroftSkill, intent_handler
import requests
import json
from mycroft.util.log import getLogger

logger = getLogger(__name__)

url = "https://mindx.mind.ai/api/v1/gateway/default/u0W0dvyUR9K_pUX5-bEZlg/2ILfgsKlSHi7bcFDc8DPnQ"
api_key = 'kq2kYszSQGesoMhXZfmpXA'
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+api_key,
}


class LeRestaurant(MycroftSkill):
    def sendHandler(self, message):
        query = message.data.get("utterance")
        data = {"query": query}
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        self.template = response_data['data']['channel-result'][0]['channel-message']['template']
        self.conversation_id = response_data['data']['conversation_id']
        headers["X-Conversation-Id"] = self.conversation_id
        self.log.info(self.template)

    def responseHandler(self):
        self.speak(self.template)

    @intent_handler('restaurant.le.intent')
    def handle_mindx_query(self, query):
        # Block all other skills from running
        self.block_all()
        # welcome!
        self.speak_dialog('restaurant.le.dialog')
        self.sendHandler(query)
        self.responseHandler()

    def shutdown(self):  # shutdown routine
        # Unblock all other skills to resume normal operation
        self.unblock_all()
        # shutdown skill
        super(LeRestaurant, self).shutdown()

def create_skill():
    return LeRestaurant()
