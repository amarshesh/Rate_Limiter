from Algorithms.tokenBucket import TokenBucket
from user_request_store import UserRequestStore
from strategy.interfaceStrategy import TokenBucketStrategy
from rate_lemiter import RateLimiter

fake_time = [1000.0]

def now():
    return fake_time[0]

# bucket config
tokenBucket = TokenBucket(capacity=3, refill_rate=1, last_refill_timestamp=now())
request_store = UserRequestStore(prototype_bucket=tokenBucket)

strategy = TokenBucketStrategy(request_store=request_store)
lim = RateLimiter(strategy)

print("\n--- Burst test (capacity = 3) ---")

print("R1", lim.is_allowed("A", now()))
print("R2", lim.is_allowed("A", now()))
print("R3", lim.is_allowed("A", now()))
print("R4", lim.is_allowed("A", now()))  # should fail

bucket = request_store.get_bucket_for_user("A")
print("tokens after burst:", bucket.tokens)

print("\n--- Wait 2 seconds (refill expected = 2 tokens) ---")

fake_time[0] += 2

print("R5", lim.is_allowed("A", now()))
print("R6", lim.is_allowed("A", now()))
print("R7", lim.is_allowed("A", now()))  # should fail again

bucket = request_store.get_bucket_for_user("A")
print("tokens after refill usage:", bucket.tokens)

print("\n--- Wait 5 seconds (bucket should refill to capacity) ---")

fake_time[0] += 5

print("R8", lim.is_allowed("A", now()))
print("R9", lim.is_allowed("A", now()))
print("R10", lim.is_allowed("A", now()))
print("R11", lim.is_allowed("A", now()))  # should fail

bucket = request_store.get_bucket_for_user("A")
print("final tokens:", bucket.tokens)