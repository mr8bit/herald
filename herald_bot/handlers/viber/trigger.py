import logging

from django.conf import settings
from viberbot.api.messages import TextMessage, KeyboardMessage
from viberbot.api.messages.picture_message import PictureMessage

from herald_bot.handlers.core.trigger import BaseTrigger
from herald_bot.handlers.utils.helpers import make_keyboard
from herald_bot.models import User

logger = logging.getLogger(__name__)


class ViberTrigger(BaseTrigger):
    """
        Вайбер триггер для State Machine
    """

    def send_keyboard(self, message, buttons, whom=None):
        """
            Отправка клавиатуры
        :param message: Текст для отправки
        :param buttons: Кнопки для отправки в формате массива
        :param whom: id чата для отправки
        :return: None
        """
        keyboard = make_keyboard(buttons)
        key_message = KeyboardMessage(tracking_data='tracking data', keyboard=keyboard)
        txt_message = TextMessage(text=message)
        self._send_messages([txt_message, key_message], whom)

    def send_message(self, message, whom=None):
        """
            Отправка сообщения
        :param message: текст сообщения
        :param whom: id чата для отпавки (необязательное)
        :return:
        """
        txt_message = TextMessage(text=message)
        self._send_messages([txt_message], whom)

    def _send_messages(self, messages, whom):
        destination = whom or self.user_id
        self.client.send_messages(destination, messages)

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

    def send_photo(self, path_image, whom=None):
        """
            Отправка фотографии
        :param image_path: Путь на самом сервере
        :return:
        """
        destination = whom or self.user_id
        site = settings.VIBER_BOT.get('WEBHOOK_SITE')
        picture = PictureMessage(
            media="{}{}{}".format(site, settings.MEDIA_URL, path_image))
        self._send_messages(picture, destination)

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
