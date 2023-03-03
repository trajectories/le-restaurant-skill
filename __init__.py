from mycroft import MycroftSkill, intent_file_handler
import requests
import json

url = "https://mindx.mind.ai/api/v1/gateway/default/u0W0dvyUR9K_pUX5-bEZlg/2ILfgsKlSHi7bcFDc8DPnQ"
api_key = 'kq2kYszSQGesoMhXZfmpXA'
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+api_key,
}
status = False


class LeRestaurant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('restaurant.le.intent')
    def handle_restaurant_le(self, message):
        # welcome!
        self.speak_dialog('restaurant.le')
        self.handle_mind_expression()
        self.start_conversation()

    def handle_mind_expression(self):
        query = "สวัสดี"
        data = {"query": query}
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        self.template = response_data['data']['channel-result'][0]['channel-message']['template']
        self.speak(self.template)
        self.conversation_id = response_data['data']['conversation_id']
        self.status = True
        self.start_conversation()

    def start_conversation(self):
        self.add_event('recognizer_loop:utterance', self.handle_utterance)

    def handle_utterance(self, message):
        if self.template != "ขอบคุณที่เข้ามาคุยกับเรานะคะ ไว้โอกาสหน้าแวะมาใหม่นะคะ ขอบคุณค่ะ":
            utterance = message.data.get('utterances')[0]
            data = {"query": utterance}
            headers["X-Conversation-Id"] = self.conversation_id
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            self.template = response_data['data']['channel-result'][0]['channel-message']['template']
            self.speak(self.template)
        else:
            self.speak(self.template)
            self.stop()

    def stop(self):
        self.status = False
        self.remove_event('recognizer_loop:utterance', self.handle_utterance)

def create_skill():
    return LeRestaurant()
