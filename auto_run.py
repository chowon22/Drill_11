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
        # 커진 몸집만큼 여유를 두고, 화면 끝에 닿으면 방향을 뒤집는다
        half_width = 50 * AutoRun.SCALE
        self.boy.x += self.boy.face_dir * AutoRun.SPEED
        if self.boy.x >= get_canvas_width() - half_width:
            self.boy.x = get_canvas_width() - half_width
            self.boy.face_dir = -1
        elif self.boy.x <= half_width:
            self.boy.x = half_width
            self.boy.face_dir = 1

    def draw(self):
        size = 100 * AutoRun.SCALE
        # 발이 땅에 붙어 있도록 커진 만큼 위로 올려 그린다
        y = self.boy.y + (size - 100) // 2
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 100, 100, 100, 100, self.boy.x, y, size, size)
        else:
            self.boy.image.clip_draw(self.boy.frame * 100, 0, 100, 100, self.boy.x, y, size, size)
