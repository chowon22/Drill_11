from pico2d import get_canvas_width


class AutoRun:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x += self.boy.face_dir * 5
        if self.boy.x >= get_canvas_width() - 50:
            self.boy.x = get_canvas_width() - 50
            self.boy.face_dir = -1
        elif self.boy.x <= 50:
            self.boy.x = 50
            self.boy.face_dir = 1

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)
