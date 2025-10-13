class WaitEvent:
    def __init__(self, duration_ms):
        self.duration = duration_ms
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        return self.timer >= self.duration