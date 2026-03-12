from time import time
from rate_limiter_rules import RateLimiterRules
class RateLimiter:
    def __init__(self):
        self.counter = {}
        self.rules = RateLimiterRules(max_requests=5, time_window=300)

    def is_allowed(self, user):
        if user not in self.counter:
            print(f"User {user} is making the first request, so allowing it.")
            timenow = time()
            self.counter[user] = {"count": 1, "time": timenow}
            return True
        else:
            count = self.counter[user]["count"]
            elapsed = time() - self.counter[user]["time"]
            if elapsed > self.rules.time_window:
                self.counter[user]["count"] = 1
                self.counter[user]["time"] = time()
                print(f"User came after {self.rules.time_window} seconds, so count is reset to 1")
                return True
            elif count < self.rules.max_requests and elapsed <= self.rules.time_window:
                self.counter[user]["count"] += 1
                print(f"Request is allowed. User has made {self.counter[user]['count']} requests in the last {int(elapsed)} seconds.")
                return True
            else:
                print(f"Rate limit exceeded. Please try again later after {self.rules.time_window - int(elapsed)} seconds")
                return False

    def print_count(self, user):
        c = self.counter.get(user, {}).get("count", 0)
        print(f"User: {user}, Count: {c}")

