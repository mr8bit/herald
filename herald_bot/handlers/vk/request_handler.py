import json
import logging

from django.conf import settings
import vk_api

from herald_bot.models import User
from herald_bot.handlers.core.state_machine import StateMachine
from herald_bot.states import BootStrapState

from herald_bot.handlers.vk.trigger import VKTrigger

from django.http import HttpResponse

logger = logging.getLogger(__name__)

def create_trigger_from_request(vk_request, vk_client):
    try:
        usr = User.objects.get(user_id=vk_request['object']['user_id']).state
    except Exception as e:
        usr = None

    trigger = VKTrigger(
        client=vk_client,
        user_id=vk_request['object']['user_id'],
        text=vk_request['object']['body'],
        messenger=2,
        user_state=usr
    )
    return trigger

class VKRequestHandler:
    _instance = None

    def __init__(self):
        vk_session = vk_api.VkApi(token=settings.VK_BOT.get('API_TOKEN'))
        self.vk_client = vk_session
        self.state_machine = StateMachine(initial_state=BootStrapState())
        self.p_msg = ''

    @classmethod
    def create_instance(cls):
        if cls._instance is None:
            cls._instance = VKRequestHandler()
        return cls._instance

    def parse(self, request):
        try:
            data = json.loads(request.body)
            if data['type'] == 'confirmation':
                return HttpResponse(settings.VK_BOT.get('CONFIRMATION_TOKEN'))
            if data['type'] != 'message_new' or self.p_msg == request.body:
                return HttpResponse()

            self.p_msg = request.body
            trigger = create_trigger_from_request(data, self.vk_client)
            self.state_machine.fire(trigger)
        except Exception as e:
            logger.warning(f'receive invalid request. {e}')
        
        return HttpResponse('ok')