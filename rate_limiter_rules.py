class RateLimiterRules:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window