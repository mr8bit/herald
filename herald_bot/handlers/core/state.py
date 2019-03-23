class BaseState:

    def __str__(self):
        """
            Название класса
        :return: Название класса
        """
        return '.'.join([self.__class__.__module__, self.__class__.__name__])

    def on_enter(self, trigger):
        """
            Срабатывает при переходе пользователя
        :param trigger:
        :return:
        """
        pass

    def on_trigger(self, trigger):
        """
            Срабатывает при отпаврки сообщения пользователем
        :param trigger:
        :return:
        """
        pass

    def on_exit(self, trigger):
        pass
