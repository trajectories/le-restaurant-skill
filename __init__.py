from mycroft import MycroftSkill, intent_file_handler
import requests
import json
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message

logger = getLogger(__name__)

url = "https://mindx.mind.ai/api/v1/gateway/default/u0W0dvyUR9K_pUX5-bEZlg/2ILfgsKlSHi7bcFDc8DPnQ"
api_key = 'kq2kYszSQGesoMhXZfmpXA'
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+api_key,
}
status = False


class LeRestaurant(MycroftSkill):
    def __init__(self):
        super(LeRestaurant, self).__init__(name="LeRestaurant")

    def initialize(self):
        # Handling settings changes
        self.add_event('LeRestaurant-skill:response', self.sendHandler)
        self.add_event('speak', self.responseHandler)
        msg = "le restaurant"
        self.bus.emit(Message('recognizer_loop:utterance', {"utterances": [
                      msg], "lang": self.lang}))  # , "session": session_id}))
        self.bus.emit(Message('speak', {"utterance": msg, "lang": self.lang}))

    def sendHandler(self, message):
        # sendData = message.data.get("utterance")
        # logger.info("Sending to Le restaurant: " + sendData)
        # Block all other skills from running
        self.block_all()
        query = "สวัสดี"
        data = {"query": query}
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        self.template = response_data['data']['channel-result'][0]['channel-message']['template']
        self.conversation_id = response_data['data']['conversation_id']
        headers["X-Conversation-Id"] = self.conversation_id

    def responseHandler(self, message):
        response = message.data.get("utterance")
        self.bus.emit(Message("LeRestaurant-skill:response",
                      {"intent_name": "LeRestaurant-response", "utterance": response}))

    def shutdown(self):  # shutdown routine
        if self.template == "ขอบคุณที่เข้ามาคุยกับเรานะคะ ไว้โอกาสหน้าแวะมาใหม่นะคะ ขอบคุณค่ะ":
            # Unblock all other skills to resume normal operation
            self.unblock_all()
        super(LeRestaurant, self).shutdown()

    # @intent_file_handler('restaurant.le.intent')
    # def handle_restaurant_le(self, message):
    #     # Block all other skills from running
    #     # self.block_all()
    #     # welcome!
    #     self.speak_dialog('restaurant.le')
    #     self.handle_mind_expression()
    #     self.start_conversation()

    # def handle_mind_expression(self):
    #     query = "สวัสดี"
    #     data = {"query": query}
    #     response = requests.post(url, headers=headers, json=data)
    #     response_data = response.json()
    #     self.template = response_data['data']['channel-result'][0]['channel-message']['template']
    #     self.speak(self.template)
    #     self.conversation_id = response_data['data']['conversation_id']
    #     self.status = True
    #     self.start_conversation()

    # def start_conversation(self):
    #     self.add_event('recognizer_loop:utterance', self.handle_utterance)

    # def handle_utterance(self, message):
    #     if self.template != "ขอบคุณที่เข้ามาคุยกับเรานะคะ ไว้โอกาสหน้าแวะมาใหม่นะคะ ขอบคุณค่ะ":
    #         utterance = message.data.get('utterances')[0]
    #         data = {"query": utterance}
    #         headers["X-Conversation-Id"] = self.conversation_id
    #         response = requests.post(url, headers=headers, json=data)
    #         response_data = response.json()
    #         self.template = response_data['data']['channel-result'][0]['channel-message']['template']
    #         self.speak(self.template)
    #     else:
    #         self.speak(self.template)
    #         self.stop()

    # def stop(self):
    #     self.status = False
    #     self.remove_event('recognizer_loop:utterance', self.handle_utterance)
    #     # Unblock all other skills to resume normal operation
    #     self.unblock_all()


def create_skill():
    return LeRestaurant()
