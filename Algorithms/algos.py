import time
import threading
from collections import deque
from interface.IAlgorithm import IAlgorithm


# 1. TOKEN BUCKET
class TokenBucket(IAlgorithm):
    def __init__(self, refill_rate=1):
        self.refill_rate = refill_rate
        self.buckets = {}
        self.lock = threading.Lock()

    def is_allowed(self, user, limit):
        with self.lock:
            uid = user.get_user_id()
            if uid not in self.buckets:
                self.buckets[uid] = {"tokens": limit, "last_refill": time.time()}
            bucket = self.buckets[uid]
            elapsed = time.time() - bucket["last_refill"]
            bucket["tokens"] = min(limit, bucket["tokens"] + elapsed * self.refill_rate)
            bucket["last_refill"] = time.time()
            if bucket["tokens"] >= 1:
                bucket["tokens"] -= 1
                return True
            return False



# 2. LEAKY BUCKET
class LeakyBucket(IAlgorithm):
    def __init__(self, leak_rate=1):
        self.leak_rate = leak_rate
        self.buckets = {}
        self.lock = threading.Lock()

    def is_allowed(self, user, limit):
        with self.lock:
            uid = user.get_user_id()
            if uid not in self.buckets:
                self.buckets[uid] = {"queue": 0, "last_leak": time.time()}
            bucket = self.buckets[uid]
            elapsed = time.time() - bucket["last_leak"]
            bucket["queue"] = max(0, bucket["queue"] - elapsed * self.leak_rate)
            bucket["last_leak"] = time.time()
            if bucket["queue"] < limit:
                bucket["queue"] += 1
                return True
            return False


# 3. FIXED WINDOW
class FixedWindow(IAlgorithm):
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.windows = {}
        self.lock = threading.Lock()

    def is_allowed(self, user, limit):
        with self.lock:
            uid = user.get_user_id()
            now = time.time()
            if uid not in self.windows:
                self.windows[uid] = {"count": 0, "window_start": now}
            window = self.windows[uid]
            if now - window["window_start"] > self.window_size:
                window["count"] = 0
                window["window_start"] = now
            if window["count"] < limit:
                window["count"] += 1
                return True
            return False


# 4. SLIDING WINDOW LOG
class SlidingWindowLog(IAlgorithm):
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.logs = {}
        self.lock = threading.Lock()

    def is_allowed(self, user, limit):
        with self.lock:
            uid = user.get_user_id()
            now = time.time()
            if uid not in self.logs:
                self.logs[uid] = deque()
            log = self.logs[uid]
            while log and log[0] <= now - self.window_size:
                log.popleft()
            if len(log) < limit:
                log.append(now)
                return True
            return False


# 5. SLIDING WINDOW COUNTER
class SlidingWindowCounter(IAlgorithm):
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.data = {}
        self.lock = threading.Lock()

    def is_allowed(self, user, limit):
        with self.lock:
            uid = user.get_user_id()
            now = time.time()
            if uid not in self.data:
                self.data[uid] = {"prev_count": 0, "curr_count": 0, "window_start": now}
            d = self.data[uid]
            elapsed = now - d["window_start"]
            if elapsed > self.window_size:
                d["prev_count"] = d["curr_count"]
                d["curr_count"] = 0
                d["window_start"] = now
            weight = 1 - (elapsed / self.window_size)
            estimated = d["prev_count"] * weight + d["curr_count"]
            if estimated < limit:
                d["curr_count"] += 1
                return True
            return False