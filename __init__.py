from mycroft import MycroftSkill, intent_handler
import requests
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message

logger = getLogger(__name__)


class LeRestaurant(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.is_active = False

    def initialize(self):
        self.url = self.settings.get('url')
        self.api_key = self.settings.get('api_key')

    @intent_handler('mindexpression.intent')
    def handle_mindexpression_intent(self, message):
        self.is_active = True
        self.speak_dialog('mindexpression.start')
        while self.is_active:
            query = self.get_response('mindexpression.query')
            if query:
                response = self.get_response_from_mindexpression(query)
                self.speak(response)
            else:
                self.is_active = False
        self.speak_dialog('mindexpression.stop')

    def get_response_from_mindexpression(self, query):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }
        data = {
            'query': query,
        }
        response = requests.post(self.url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            return response_data.get('message', '')
        else:
            self.log.error(f'Request to MindExpression failed with status code {response.status_code}.')
            return 'Sorry, I could not get a response from the chatbot.'

    def stop(self):
        self.is_active = False

def create_skill():
    return MindExpressionSkill()
