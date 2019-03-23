import importlib


class StateMachine:
    """
        Машина состояния
    """

    def __init__(self, initial_state):
        self.initial_state = initial_state

    def fire(self, trigger):
        self.state = trigger.state

        print('STATE BEFORE', self.state)

        if self.state is None:
            self.state = self.initial_state
            new_state = self.state.on_trigger(trigger)
            # self.state.on_enter(trigger)
            # trigger.get_user().state = self.state
        else:
            module_name, class_name = self.state.rsplit(".", 1)
            instance = getattr(importlib.import_module(module_name), class_name)
            self.state = instance()
            new_state = self.state.on_trigger(trigger)
            try:
                instance = getattr(importlib.import_module(new_state.__module__), new_state.__name__)
                new_state = instance()
            except Exception as e:
                pass
        usr = trigger.get_user()
        usr.state = new_state
        usr.save()
        self.to_state(new_state, trigger)

        trigger.state = self.state

    def to_state(self, new_state, trigger):
        if not new_state:
            return self.state

        if new_state == self.state:
            reenter_state = self.state.on_enter(trigger)
            self.to_state(reenter_state, trigger)
            return

        exit_state = self.state.on_exit(trigger)
        if exit_state:
            self.to_state(exit_state, trigger)
            return

        self.state = new_state

        enter_state = self.state.on_enter(trigger)
        if enter_state:
            self.to_state(enter_state, trigger)
            return
