import threading

class TokenBucket:

    def __init__(self, capacity, refill_rate, last_refill_timestamp):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.last_refill_timestamp = last_refill_timestamp
        self.tokens = capacity
        self.lock = threading.Lock()

    def try_consume(self, tokens, timestamp):    # ye ab dono refill and cosume ko single threaded me hi use karega taki race contion na bane
        with self.lock:
            time_passed = max(0, timestamp - self.last_refill_timestamp)
            tokens_to_add = time_passed * self.refill_rate

            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill_timestamp = timestamp

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            return False