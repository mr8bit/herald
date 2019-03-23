from herald_bot.handlers.core.state import BaseState as State


class BootStrapState(State):
    def on_trigger(self, trigger):
        trigger.send_message("Привет, это Herald, я один и я везде")
        return BootStrapState()
