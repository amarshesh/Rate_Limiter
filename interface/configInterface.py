# config/rate_limit_config.py

from abc import ABC, abstractmethod
from enitty.subscription import SubscriptionType
class IRateLimitConfig(ABC):
    @abstractmethod
    def get_limit(self, subscription_type) -> int:
        pass


# Default implementation
class DefaultRateLimitConfig(IRateLimitConfig):
    SUBSCRIPTION_LIMITS = {
        SubscriptionType.FREE: 10,
        SubscriptionType.PREMIUM: 100,
        SubscriptionType.PRO_USER: 1000,
    }

    def get_limit(self, subscription_type) -> int:
        return self.SUBSCRIPTION_LIMITS.get(subscription_type, 0)


# Kal naya plan aaya — sirf extend karo, touch mat karo Default ✅
class EnterpriseRateLimitConfig(IRateLimitConfig):
    SUBSCRIPTION_LIMITS = {
        SubscriptionType.FREE: 20,
        SubscriptionType.PREMIUM: 200,
        SubscriptionType.PRO_USER: 2000,
        SubscriptionType.ENTERPRISE: 10000,  # naya!
    }

    def get_limit(self, subscription_type) -> int:
        return self.SUBSCRIPTION_LIMITS.get(subscription_type, 0)