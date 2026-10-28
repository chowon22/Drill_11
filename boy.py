from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from state_machine import StateMachine
from idle import Idle
from sleep import Sleep
from run import Run


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def arrow_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key in (SDLK_LEFT, SDLK_RIGHT)


def arrow_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key in (SDLK_LEFT, SDLK_RIGHT)


def time_out(e):
    return e[0] == 'TIME_OUT'


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.RUN = Run(self)
        moving = lambda e: self.dir != 0
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: [(time_out, self.SLEEP),
                            (lambda e: (arrow_down(e) or arrow_up(e)) and moving(e), self.RUN)],
                self.SLEEP: [(space_down, self.IDLE),
                             (lambda e: (arrow_down(e) or arrow_up(e)) and moving(e), self.RUN)],
                self.RUN: [(lambda e: (arrow_down(e) or arrow_up(e)) and not moving(e), self.IDLE)],
            }
        )

    def handle_event(self, event):
        if event.type in (SDL_KEYDOWN, SDL_KEYUP) and event.key in (SDLK_LEFT, SDLK_RIGHT):
            # 눌린 방향키를 더하고 뗀 방향키를 빼서, 양쪽을 동시에 눌러도 dir이 맞게 유지된다
            step = 1 if event.key == SDLK_RIGHT else -1
            self.dir += step if event.type == SDL_KEYDOWN else -step
        self.state_machine.handle_state_event(('INPUT', event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
