class RateLimiter:
    def __init__(self, strategy):
        self.strategy = strategy

    def is_allowed(self, user, timestamp):
        return self.strategy.selected_algorithm(user, timestamp)

        