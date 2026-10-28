from pico2d import get_canvas_width


class AutoRun:
    SPEED = 15
    SCALE = 2

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x += self.boy.face_dir * AutoRun.SPEED
        if self.boy.x >= get_canvas_width() - 50:
            self.boy.x = get_canvas_width() - 50
            self.boy.face_dir = -1
        elif self.boy.x <= 50:
            self.boy.x = 50
            self.boy.face_dir = 1

    def draw(self):
        size = 100 * AutoRun.SCALE
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y, size, size)
        else:
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y, size, size)
