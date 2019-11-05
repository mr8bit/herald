import json
import logging

from django.conf import settings
import vk_api
import datetime
import pytz
from herald_bot.models import User, Request, Error
from herald_bot.handlers.core.state_machine import StateMachine
from herald_bot.states import BootStrapState

from herald_bot.handlers.vk.trigger import VKTrigger
from requests.exceptions import ConnectionError
from django.http import HttpResponse

logger = logging.getLogger(__name__)
session = vk_api.VkApi(token=settings.VK_BOT.get('API_TOKEN'))
api_vk = session.get_api()

import asyncio

def create_trigger_from_request(vk_request, vk_client):
    try:
        usr = User.objects.get(user_id=vk_request['object']['user_id'])
    except Exception as e:
        usr = None
    Request.create_request(user=usr, state=usr.state, text=vk_request['object']['body'])
    trigger = VKTrigger(
        client=vk_client,
        user_id=vk_request['object']['user_id'],
        text=vk_request['object']['body'],
        messenger=2,
        user_state=usr.state,
        api=api_vk
    )
    return trigger


class VKRequestHandler:
    _instance = None

    def __init__(self):
        self.vk_client = session
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
                return HttpResponse("ok")
            today = datetime.datetime.now()
            delta = datetime.timedelta(minutes=1)
            request_datetime = datetime.datetime.fromtimestamp(int(data['object']['date']))
            if today - request_datetime < delta:
                self.p_msg = request.body
                trigger = create_trigger_from_request(data, self.vk_client)
                self.state_machine.fire(trigger)

        except ConnectionError as e: # Если произошел обрыв сети
            logger.warning(f'{e}, try to connection')

            data = json.loads(request.body)
            if data['type'] == 'confirmation':
                print(data)
                return HttpResponse(settings.VK_BOT.get('CONFIRMATION_TOKEN'))
            if data['type'] != 'message_new' or self.p_msg == request.body:
                return HttpResponse("ok")
            self.p_msg = request.body

            try:
                usr = User.objects.get(user_id=self.p_msg['object']['user_id'])
            except Exception as e:
                usr = None
            Error.create_request(user=usr, state=usr.state, text=self.p_msg['object']['body'])

            trigger = create_trigger_from_request(data, self.vk_client)
            self.state_machine.fire(trigger)

        except Exception as e:
            logger.error(f'receive invalid request. {e}')

        return HttpResponse('ok')
