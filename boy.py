from pico2d import load_image, get_time, clamp, get_canvas_width, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from transitions import Machine


class Boy:
    states = ['IDLE', 'SLEEP', 'RUN']
    transitions = [
        {'trigger': 'time_out', 'source': 'IDLE', 'dest': 'SLEEP'},
        {'trigger': 'space_down', 'source': 'SLEEP', 'dest': 'IDLE'},
        {'trigger': 'arrow_down', 'source': 'IDLE', 'dest': 'RUN', 'conditions': 'is_moving'},
        {'trigger': 'arrow_up', 'source': 'IDLE', 'dest': 'RUN', 'conditions': 'is_moving'},
        {'trigger': 'arrow_down', 'source': 'SLEEP', 'dest': 'RUN', 'conditions': 'is_moving'},
        {'trigger': 'arrow_up', 'source': 'SLEEP', 'dest': 'RUN', 'conditions': 'is_moving'},
        {'trigger': 'arrow_down', 'source': 'RUN', 'dest': 'IDLE', 'unless': 'is_moving'},
        {'trigger': 'arrow_up', 'source': 'RUN', 'dest': 'IDLE', 'unless': 'is_moving'},
    ]

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(model=self, states=Boy.states, transitions=Boy.transitions,
                               initial='IDLE', ignore_invalid_triggers=True)
        self.on_enter_IDLE()

    def on_enter_IDLE(self):
        self.wait_start_time = get_time()

    def is_moving(self):
        return self.dir != 0

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.space_down()
        elif event.type in (SDL_KEYDOWN, SDL_KEYUP) and event.key in (SDLK_LEFT, SDLK_RIGHT):
            # 눌린 방향키를 더하고 뗀 방향키를 빼서, 양쪽을 동시에 눌러도 dir이 맞게 유지된다
            step = 1 if event.key == SDLK_RIGHT else -1
            if event.type == SDL_KEYDOWN:
                self.dir += step
                self.arrow_down()
            else:
                self.dir -= step
                self.arrow_up()
            if self.dir != 0 and self.state != 'SLEEP':
                self.face_dir = self.dir

    def update(self):
        self.frame = (self.frame + 1) % 8
        if self.state == 'IDLE' and get_time() - self.wait_start_time > 5:
            self.time_out()
        elif self.state == 'RUN':
            self.x = clamp(50, self.x + self.dir * 5, get_canvas_width() - 50)

    def draw(self):
        if self.state == 'IDLE':
            if self.face_dir == 1:
                self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
        elif self.state == 'SLEEP':
            if self.face_dir == 1:
                self.image.clip_composite_draw(self.frame * 100, 300, 100, 100,
                                               3.141592 / 2, '', self.x - 25, self.y - 25, 100, 100)
            else:
                self.image.clip_composite_draw(self.frame * 100, 200, 100, 100,
                                               -3.141592 / 2, '', self.x + 25, self.y - 25, 100, 100)
        elif self.state == 'RUN':
            if self.face_dir == 1:
                self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
