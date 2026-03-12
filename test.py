# test_rate.py
from rate_lemiter import RateLimiter
import rate_lemiter

fake_time = [1000.0]
def now():
    return fake_time[0]
rate_lemiter.time = now

lim = RateLimiter()

# Scenario A: 6 rapid requests (within window)
print("A1", lim.is_allowed("A"))  # True (1)
fake_time[0] += 10
print("A2", lim.is_allowed("A"))  # True (2)
fake_time[0] += 10
print("A3", lim.is_allowed("A"))  # True (3)
fake_time[0] += 10
print("A4", lim.is_allowed("A"))  # True (4)
fake_time[0] += 10
print("A5", lim.is_allowed("A"))  # True (5)
fake_time[0] += 10
print("A6", lim.is_allowed("A"))  # False (exceeded)

# Scenario B: after >300s window reset
fake_time[0] += 301
print("A_after_reset", lim.is_allowed("A"))  # True (reset to 1)

# Scenario C: exact boundary at 300s
fake_time[0] = 5000.0
print("B1", lim.is_allowed("B"))  # True (1)
fake_time[0] += 300.0
print("B_at_300s", lim.is_allowed("B"))  # True (counts as inside window)

# Scenario D: independent users
print("C1 (new user C)", lim.is_allowed("C"))  # True