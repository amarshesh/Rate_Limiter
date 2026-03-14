from Algorithms.tokenBucket import TokenBucket
import threading


class UserRequestStore:
    def __init__(self, capacity=None, refill_rate=None, last_refill_timestamp=None, prototype_bucket=None, ttl=300):
        self.user_request_store = {}
        self.ttl = ttl
        self.lock = threading.Lock()

        if prototype_bucket is not None:
            self.capacity = prototype_bucket.capacity
            self.refill_rate = prototype_bucket.refill_rate
            self.last_refill_timestamp = prototype_bucket.last_refill_timestamp
        else:
            self.capacity = capacity
            self.refill_rate = refill_rate
            self.last_refill_timestamp = last_refill_timestamp

    def get_bucket_for_user(self, user):
        with self.lock:
            bucket = self.user_request_store.get(user)
            if bucket:
                bucket.last_request_timestamp = bucket.last_request_timestamp
            return bucket

    def add_bucket_for_user(self, user, timestamp=None):
        with self.lock:
            if user not in self.user_request_store:
                last = timestamp if timestamp is not None else self.last_refill_timestamp
                bucket = TokenBucket(
                    capacity=self.capacity,
                    refill_rate=self.refill_rate,
                    last_refill_timestamp=last
                )
                bucket.last_request_timestamp = last
                self.user_request_store[user] = bucket

    def cleanup_expired_buckets(self, current_timestamp):
        expired_users = []

        with self.lock:
            for user, bucket in self.user_request_store.items():
                last_seen = getattr(bucket, "last_request_timestamp", bucket.last_refill_timestamp)

                if current_timestamp - last_seen > self.ttl:
                    expired_users.append(user)

            for user in expired_users:
                del self.user_request_store[user]