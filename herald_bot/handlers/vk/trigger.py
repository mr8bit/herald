import logging

import vk_api
from django.conf import settings
from herald_bot.handlers.core.trigger import BaseTrigger

from herald_bot.handlers.core.trigger import BaseTrigger
from herald_bot.handlers.utils.helpers import make_keyboard_vk
from herald_bot.models import User

from vk_api.utils import get_random_id

logger = logging.getLogger(__name__)


class VKTrigger(BaseTrigger):
    """
        VK триггер для State Machine
    """
    def __init__(self, client, user_id, messenger, text, user_state, api):
        super(VKTrigger, self).__init__(client, user_id, messenger, text, user_state, api)
        self.api = api

    def send_keyboard(self, message, buttons, whom=None):
        """
            Отправка клавиатуры
        :param message: Текст для отправки
        :param buttons: Кнопки для отправки в формате массива
        :param whom: id чата для отправки
        :return: None
        """
        self.api.messages.send(
            user_id=self.user_id,
            message=message,
            random_id=get_random_id(),
            keyboard=make_keyboard_vk(buttons)
        )

    def send_message(self, message, whom=None):
        self.api.messages.send(
            user_id=self.user_id,
            message=message,
            random_id=get_random_id())

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
        upload = vk_api.VkUpload(self.client)
        photo = upload.photo_messages(image_path)[0]
        attachment = f"photo{photo['owner_id']}_{photo['id']}"
        self.client.get_api().messages.send(
            user_id=self.user_id,
            random_id=get_random_id(),
            attachment=attachment)

    def send_file(self, file_path):
        """
            Отправка документа
       :param file_path: Путь на самом сервере
       :return:
        """
        upload = vk_api.VkUpload(self.client)
        document = upload.document_message(file_path)[0]
        attachment = f"doc{document['owner_id']}_{document['id']}"
        self.client.get_api().messages.send(
            user_id=self.user_id,
            random_id=get_random_id(),
            attachment=attachment)
