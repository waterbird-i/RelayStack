class TokenBucket:
    def __init__(self, rate_per_second, capacity, now=0.0):
        self.rate_per_second = rate_per_second
        self.capacity = capacity
        self.tokens = capacity
        self.updated_at = now

    def allow(self, cost=1, now=0.0):
        elapsed = int(now - self.updated_at)
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_second)
        self.updated_at = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False
