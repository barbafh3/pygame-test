class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Collision:
    def __init__(self, left, right, top, bottom):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right


class Direction:
    def __init__(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
