from enitty.subscription import SubscriptionType


class RateLimitConfig:
    SUBSCRIPTION_LIMITS = {
        SubscriptionType.FREE: 10,
        SubscriptionType.PREMIUM: 100,
        SubscriptionType.PRO_USER: 1000,
    }
    
    @staticmethod
    def get_limit(subscription_type):
        return RateLimitConfig.SUBSCRIPTION_LIMITS.get(subscription_type, 0)