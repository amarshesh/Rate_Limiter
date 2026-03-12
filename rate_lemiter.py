class RateLimiter:

    def __init__(self, user):
        self.user = user
        self.count = {}

    def is_allowed(self):
        if self.count.get(self.user, 0) >= 3:
            return False
        else:
            self.count[self.user] = self.count.get(self.user, 0) + 1
            return True

    def print_count(self):
        print(f"User: {self.user}, Count: {self.count[self.user]}")


# Example usage
user1 = "User1"
limiter1 = RateLimiter(user1)
print(limiter1.is_allowed())  # 
print(limiter1.is_allowed())  # 
print(limiter1.is_allowed())  # 
print(limiter1.is_allowed())  # True