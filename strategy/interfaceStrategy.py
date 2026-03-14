
from abc import ABC, abstractmethod
import time
class RateLimiterAlgoStrategy(ABC):
    @abstractmethod
    def selected_algorithm(self, user, timestamp):
        pass
    
class TokenBucketStrategy(RateLimiterAlgoStrategy):

    def __init__(self, request_store):
        self.request_store = request_store

    def selected_algorithm(self, user, timestamp, token_required=1):

        bucket = self.request_store.get_bucket_for_user(user)

        if bucket is None:
            self.request_store.add_bucket_for_user(user, timestamp)
            bucket = self.request_store.get_bucket_for_user(user)

        return bucket.try_consume(token_required, timestamp)
    
    def delete_background_expired_buckets(self, current_timestamp):
        self.request_store.cleanup_expired_buckets(time())

class LeakyBucketStrategy(RateLimiterAlgoStrategy):
    def __init__(self, request_store):
        self.request_store = request_store

    def selected_algorithm(self, user, timestamp):
        return "LeakyBucketStrategy selected for user: {}".format(user)
    
class SlidingWindowStrategy(RateLimiterAlgoStrategy):
    def __init__(self, rules, request_store):
        self.rules = rules
        self.request_store = request_store

    def selected_algorithm(self, user, timestamp):
        return "SlidingWindowStrategy selected for user: {}".format(user)

class SlidingWindowCounterStrategy(RateLimiterAlgoStrategy):
    def __init__(self, rules, request_store):
        self.rules = rules
        self.request_store = request_store

    def selected_algorithm(self, user, timestamp):
        return "SlidingWindowCounterStrategy selected for user: {}".format(user)
    

class FixedWindowStrategy(RateLimiterAlgoStrategy):
    def __init__(self, rules, request_store):
        self.rules = rules
        self.request_store = request_store

    def selected_algorithm(self, user, timestamp):
        return "FixedWindowStrategy selected for user: {}".format(user)
    

class FixedWindowCounterStrategy(RateLimiterAlgoStrategy):
    def __init__(self, rules, request_store):
        self.rules = rules
        self.request_store = request_store

    def selected_algorithm(self, user, timestamp):
        return "FixedWindowCounterStrategy selected for user: {}".format(user)