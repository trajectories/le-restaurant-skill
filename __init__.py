from mycroft import MycroftSkill, intent_file_handler
import requests
import json

url = "https://mindx.mind.ai/api/v1/gateway/default/u0W0dvyUR9K_pUX5-bEZlg/2ILfgsKlSHi7bcFDc8DPnQ"
api_key = 'kq2kYszSQGesoMhXZfmpXA'
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+api_key,
}


class LeRestaurant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('restaurant.le.intent')
    def handle_restaurant_le(self, message):
        # welcome!
        self.speak_dialog('restaurant.le')
        self.handle_send_message_to_mind_expression()

    def handle_send_message_to_mind_expression(self):
        query = "สวัสดี"
        data = {"query": query}
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        templete = response_data['data']['channel-result'][0]['channel-message']['template']
        conversation_id = response_data['data']['conversation_id']
        self.speak(templete)
        self.speak(conversation_id)


def create_skill():
    return LeRestaurant()
