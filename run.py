from pico2d import clamp, get_canvas_width


class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.face_dir = self.boy.dir

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        if self.boy.dir != 0:
            self.boy.face_dir = self.boy.dir
        self.boy.x = clamp(50, self.boy.x + self.boy.dir * 5, get_canvas_width() - 50)

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, self.boy.y)
