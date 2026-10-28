class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(('START', None))

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, state_event):
        for check_event, next_state in self.rules[self.cur_state]:
            if check_event(state_event):
                self.cur_state.exit(state_event)
                self.cur_state = next_state
                self.cur_state.enter(state_event)
                return
