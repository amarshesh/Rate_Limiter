from config.rate_limit_entity import RateLimitConfig
from enitty.user import User
from enitty.subscription import SubscriptionType
from Algorithms.algos import TokenBucket, LeakyBucket, FixedWindow, SlidingWindowCounter, SlidingWindowLog
from rateLimiter import RateLimiter
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

rate_limiter = RateLimiter(algorithm=FixedWindow(), config=RateLimitConfig)
# FREE - 10 limit
user1 = User(1, "Alice", SubscriptionType.FREE, 5)    # allow
user2 = User(2, "Bob", SubscriptionType.FREE, 10)     # deny

# PREMIUM - 100 limit  
user3 = User(3, "Charlie", SubscriptionType.PREMIUM, 50)   # allow
user4 = User(4, "Dave", SubscriptionType.PREMIUM, 100)     # deny

for user in [user1, user2, user3, user4]:
    result = rate_limiter.is_request_allowed(user)
    print(f"{user.get_name()} → {'✅ Allow' if result else '❌ Deny'}")