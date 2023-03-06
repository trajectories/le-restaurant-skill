from mycroft import MycroftSkill, intent_handler
import requests
import json

url = "https://mindx.mind.ai/api/v1/gateway/default/u0W0dvyUR9K_pUX5-bEZlg/2ILfgsKlSHi7bcFDc8DPnQ"
api_key = 'kq2kYszSQGesoMhXZfmpXA'


class LeRestaurant(MycroftSkill):
    def __init__(self):
        super().__init__(name="LeRestaurant")

    def initialize(self):
        # Initialize conversation ID
        self.conversation_id = None

    def handle_mindx_response(self, msg):
        # Send query to MindX API and retrieve response
        data = {"query": msg}
        # headers = {"Content-Type": "application/json",
        #            "Authorization": "Bearer " + {self.settings.get('api_key')}}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+api_key,
        }
        if self.conversation_id is not None:
            headers["X-Conversation-Id"] = self.conversation_id
        # response = requests.post(self.settings.get(
        #     'url'), headers=headers, json=data)
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        self.template = response_data['data']['channel-result'][0]['channel-message']['template']
        self.conversation_id = response_data['data']['conversation_id']

    @intent_handler('restaurant.le.intent')
    def handle_restaurant_le(self, message):
        self.log.info("Le Restaurant skill is running")
        # Block all other skills from running
        msg = message.data.get('utterance')
        self.block_all()
        self.handle_mindx_response(msg)
        self.speak(self.template)
        # Listen to user input until the user says "ขอบคุณครับ"
        while self.template != "ขอบคุณที่เข้ามาคุยกับเรานะคะ ไว้โอกาสหน้าแวะมาใหม่นะคะ ขอบคุณค่ะ":
            msg = message.data.get('utterance')
            self.handle_mindx_response(msg)
            self.speak(self.template)
        # Unblock all other skills to resume normal operation
        self.unblock_all()

    def shutdown(self):
        # Unblock all other skills to resume normal operation
        self.unblock_all()
        super().shutdown()


def create_skill():
    return LeRestaurant()
