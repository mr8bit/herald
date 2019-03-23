from django.conf import settings
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.viber_requests import (
    ViberMessageRequest, ViberSubscribedRequest, ViberFailedRequest
)

from herald_bot.models import User
from herald_bot.handlers.core.state_machine import StateMachine
from herald_bot.states import BootStrapState
from .trigger import ViberTrigger as Trigger


def _get_bot_configuration():
    return BotConfiguration(
        name=settings.VIBER_BOT.get('VIBER_BOT_NAME'),
        auth_token=settings.VIBER_BOT.get('VIBER_AUTH_TOKEN'),
        avatar=settings.VIBER_BOT.get('VIBER_AVATAR'),
    )


def create_trigger_from_request(viber_request, viber_client):
    try:
        usr = User.objects.get(user_id=viber_request.sender.id).state
    except Exception as e:
        usr = None
    return Trigger(
        client=viber_client,
        user_id=viber_request.sender.id,
        text=viber_request.message.text,
        messenger=1,
        user_state=usr
    )


class ViberRequestHandler:
    _instance = None

    def __init__(self):
        bot_config = _get_bot_configuration()
        self.viber_client = Api(bot_config)
        self.state_machine = StateMachine(initial_state=BootStrapState())

    @classmethod
    def create_instance(cls):
        if cls._instance is None:
            cls._instance = ViberRequestHandler()

        return cls._instance

    def parse(self, request):
        viber_request = self.viber_client.parse_request(request.body)
        if isinstance(viber_request, (ViberSubscribedRequest, ViberMessageRequest)):
            trigger = create_trigger_from_request(viber_request, self.viber_client)
            # получение пользовательского id - viber_request.sender.id
            # получение время обращения timestamp - viber_request.timestamp
            # сохранение статистики
            self.state_machine.fire(trigger)

        elif isinstance(viber_request, ViberFailedRequest):
            pass
