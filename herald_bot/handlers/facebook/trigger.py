import logging

from django.conf import settings
from herald_bot.handlers.core.trigger import BaseTrigger

from pymessenger.bot import Bot

from herald_bot.handlers.core.trigger import BaseTrigger
from herald_bot.models import User

logger = logging.getLogger(__name__)

class FacebookTrigger(BaseTrigger):
    """
        Facebook триггер для State Machine
    """

    def send_keyboard(self, message, buttons, whom=None):
        """
            Отправка клавиатуры
        :param message: Текст для отправки
        :param buttons: Кнопки для отправки в формате массива
        :param whom: id чата для отправки
        :return: None
        """

        self.client.send_message(self.user_id, {
            "text": message,
            "quick_replies":[{ 
                "content_type" : "text",
                "title": b,
                "payload": b
                } for b in buttons]
        })

    def send_message(self, message, whom=None):
        self.client.send_text_message(self.user_id, message)

    def get_user(self, whom=None):
        """
            Получение пользователя из базы данных
        :param whom: id пользователя
        :return: User объект пользователя
        """
        try:
            return User.objects.get(user_id=self.user_id)
        except Exception as e:
            logger.error("Error on get user: {}".format(e))
            return False


    def create_user(self):
        """
            Создание пользователя
        :return: None
        """
        try:
            new_user = User.objects.create(user_id=self.user_id, messenger=self.messenger)
            new_user.save()
        except Exception as e:
            logger.error("Error on crete user: {}".format(e))


    def send_photo(self, image_path):
        """
            Отправка фотографии
        :param image_path: Путь на самом сервере
        :return:
        """
        
        self.client.send_image(self.user_id, image_path)