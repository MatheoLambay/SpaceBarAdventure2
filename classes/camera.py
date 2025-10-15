
class Camera:
    def __init__(self, width, height, win_width, win_height):
        self.width = width
        self.height = height
        self.win_width = win_width
        self.win_height = win_height
        self.x = 0
        self.y = 0

    def apply(self, rect):
        return rect.move(-self.x, -self.y)

    def update(self, target):
        self.x = target.rect.centerx - self.win_width // 2
        self.y = target.rect.centery - self.win_height // 2
        self.x = max(0, min(self.x, self.width - self.win_width))
        self.y = max(0, min(self.y, self.height - self.win_height))
