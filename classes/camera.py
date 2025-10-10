
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def apply(self, rect):
        return rect.move(-self.x, -self.y)

    def update(self, target):
        self.x = target.rect.centerx - 400
        self.y = target.rect.centery - 300
        self.x = max(0, min(self.x, self.width - 800))
        self.y = max(0, min(self.y, self.height - 600))
