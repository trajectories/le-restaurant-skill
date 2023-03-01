from mycroft import MycroftSkill, intent_file_handler


class LeRestaurant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('restaurant.le.intent')
    def handle_restaurant_le(self, message):
        self.speak_dialog('restaurant.le')


def create_skill():
    return LeRestaurant()

