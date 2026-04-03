    
from itertools import count


class User:
    def __init__(self, user_id, name, subscription_type, request_count=0):
        self.user_id = user_id   # kind of user ip.
        self.name = name
        self.subscription_type = subscription_type
        self.request_count = request_count


    def get_user_id(self):
        return self.user_id
    def get_name(self):
        return self.name
    def get_subscription_type(self):
        return self.subscription_type
    def get_request_count(self):
        return self.request_count
    def set_request_count(self, count):
        self.request_count = count

    def increment_request_count(self, delta=1):
        self.request_count += delta