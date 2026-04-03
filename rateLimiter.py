import logging
from config.rate_limit_entity import RateLimitConfig
from interface.IAlgorithm import IAlgorithm

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, algorithm: IAlgorithm, config=RateLimitConfig):
        self.algorithm = algorithm
        self.config = config

    def is_request_allowed(self, user) -> bool:
        limit = self.config.get_limit(user.get_subscription_type())
        allowed = self.algorithm.is_allowed(user, limit)
        if allowed:
            # use increment helper to avoid caller computing new value
            if hasattr(user, 'increment_request_count'):
                user.increment_request_count(1)
            else:
                user.set_request_count(user.get_request_count() + 1)
            logger.info(
                "Request allowed for user: %s with subscription type: %s",
                user.get_name(),
                user.get_subscription_type().name,
            )
        else:
            logger.info(
                "Request denied for user: %s with subscription type: %s",
                user.get_name(),
                user.get_subscription_type().name,
            )
        return allowed


