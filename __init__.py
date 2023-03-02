from mycroft import MycroftSkill, intent_file_handler
import requests
import json

url = "https://mindx.mind.ai/api/v1/gateway/default/u0W0dvyUR9K_pUX5-bEZlg/2ILfgsKlSHi7bcFDc8DPnQ"
api_key = "kq2kYszSQGesoMhXZfmpXA"


class LeRestaurant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        
        

    @intent_file_handler('restaurant.le.intent')
    def handle_restaurant_le(self, message):
        self.speak_dialog('restaurant.le')
        self.headers = {
        	"Content-Type": "application/json",
        	"Authorization": f"Bearer {api_key}",
        }
        self.speak('this is my statement')
        data = {"query": "hi"}
        response = requests.post(url, headers=self.headers, json=data)
        response_data = response.json()
        for channel_result in response_data.get('data', {}).get('channel-result', []):
        	for channel_message in channel_result.get('channel-message', []):
        		if channel_messasge.get('templete-type') == 'text':
        			message = channel_message.get('templete')
        print("=========>MindExpression", message)
"""
    def handle_mind_expression_query(self, message):
    	self.headers = {
        	'Content-Type': 'application/json',
        	'Authorization': {self.api_key},
        }
    	self.query = message.date.get('query')
    	self.data = {
    		'query': {self.query}
    	}
	response = requests.post(self.url, headers=self.headers, json=self.data)
	response_data = response.json().["data"]
	print("MindExpresssssssssssssssssssion", response_data)
"""


def create_skill():
    return LeRestaurant()
