import importlib
import asyncio
import datetime
class StateMachine:
    """
        Машина состояния
    """

    def __init__(self, initial_state):
        """

        :param initial_state: Начальное состояние пользователя, там где он всегда нахохиться
        """
        self.initial_state = initial_state

    @staticmethod
    def str_to_class(str):
        module_name, class_name = str.rsplit(".", 1)
        instance = getattr(importlib.import_module(module_name), class_name)
        return instance

    def fire(self, trigger):
        self.state = trigger.state

        print('STATE BEFORE', self.state)

        if self.state is None:  # Если экран не был передан, или пользователь только зашел
            try:  # Если было предыдущее состояние
                prev_state = trigger.get_user().prev_state
                instance = self.str_to_class(prev_state)
                self.state = instance()
                print("0 Идем к  " + str(self.state) + str(datetime.datetime.now()))
                new_state = self.state.on_trigger(trigger)
                print("0 Вышли из " + str(self.state)+ str(datetime.datetime.now()))
            except:  # Если пользователь только зашел, то шлем его на начальный экран
                self.state = self.initial_state
                print("1 Идем к  " + str(self.state)+ str(datetime.datetime.now()))
                new_state = self.state.on_trigger(trigger)
                print("1 Вышли из " + str(self.state)+ str(datetime.datetime.now()))

        else:  # Знаем на какой экран идти
            instance = self.str_to_class(self.state)
            self.state = instance()
            print("2 Идем к  "+ str(self.state)+ str(datetime.datetime.now()))
            new_state = self.state.on_trigger(trigger)
            print("2 Вышли из " + str(self.state)+ str(datetime.datetime.now()))

        usr = trigger.get_user()
        usr.state = new_state  # текущее положение пользователя
        usr.prev_state = self.state  # прошлое положение пользователя
        usr.save()
        print('SAVE STATE', new_state)

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
