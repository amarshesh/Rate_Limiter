import redis
import time
from interface.IAlgorithm import IAlgorithm

class DistributedTokenBucket(IAlgorithm):
    
    def __init__(self, refill_rate=1):
        self.refill_rate = refill_rate
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def is_allowed(self, user, limit) -> bool:
        uid = user.get_user_id()
        token_key = f"tokens:{uid}"
        time_key  = f"last_refill:{uid}"

        # Atomic operation — race condition nahi hoga ✅
        with self.redis.pipeline() as pipe:
            try:
                pipe.watch(token_key, time_key)
                
                now = time.time()
                tokens = pipe.get(token_key)
                last_refill = pipe.get(time_key)

                # Pehli baar user aa raha hai
                tokens = float(tokens) if tokens else limit
                last_refill = float(last_refill) if last_refill else now

                # Refill karo
                elapsed = now - last_refill
                tokens = min(limit, tokens + elapsed * self.refill_rate)

                pipe.multi()

                if tokens >= 1:
                    pipe.set(token_key, tokens - 1)
                    pipe.set(time_key, now)
                    pipe.execute()
                    return True
                else:
                    pipe.execute()
                    return False

            except redis.WatchError:
                # Koi aur request aa gayi same time pe — retry
                return self.is_allowed(user, limit)