class BaseTrigger:
    """
        Базовый триггер
    """

    def __init__(self, client, user_id, messenger, text, user_state):
        """
            Инициализация класса
        :param client: API для работы и отпаврки сообщений
        :param user_id: id пользователя для отправки сообщения
        :param messenger: Мессенджер с коротого пришло сообщение
        :param text: текст от пользователя
        :param user_state: состояние пользователя
        """
        self.client = client
        self.text = text
        self.messenger = messenger
        self.user_id = user_id
        self.state = user_state

    def send_keyboard(self, message, buttons, whom=None):
        pass

    def send_message(self, message, whom=None):
        pass

    def get_user(self, whom=None):
        pass

    def create_user(self):
        pass

    def send_photo(self, image_path):
        pass
