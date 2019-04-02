import json
import logging

from django.conf import settings

from herald_bot.models import User
from herald_bot.handlers.core.state_machine import StateMachine
from herald_bot.states import BootStrapState

from pymessenger.bot import Bot

from herald_bot.handlers.facebook.trigger import FacebookTrigger

from django.http import HttpResponse

import traceback

logger = logging.getLogger(__name__)

def create_trigger_from_request(facebook_request, facebook_client):
    recipient_id = facebook_request['sender']['id']
    message = facebook_request['message']['text']

    try:
        usr = User.objects.get(user_id=recipient_id).state
    except Exception as e:
        usr = None

    trigger = FacebookTrigger(
        client=facebook_client,
        user_id=recipient_id,
        text=message,
        messenger=3,
        user_state=usr
    )
    return trigger

class FacebookRequestHandler:
    _instance = None

    def __init__(self):
        self.facebook_client = Bot(settings.FACEBOOK_BOT.get('ACCESS_TOKEN'))
        self.state_machine = StateMachine(initial_state=BootStrapState())

    @classmethod
    def create_instance(cls):
        if cls._instance is None:
            cls._instance = FacebookRequestHandler()
        return cls._instance

    def parse(self, request):
        try:
            if request.method == 'GET':
                """Before allowing people to message your bot, Facebook has implemented a verify token
                that confirms all requests that your bot receives came from Facebook.""" 
        
                token_sent = request.GET['hub.verify_token']
                if token_sent == settings.FACEBOOK_BOT.get('VERIFY_TOKEN'):
                    return HttpResponse(request.GET['hub.challenge'])
            else:
                data = json.loads(request.body)
                for event in data['entry']:
                    messaging = event['messaging']
                    for x in messaging:
                        if x.get('message') and x['message'].get('text'):
                            trigger = create_trigger_from_request(x, self.facebook_client)
                            self.state_machine.fire(trigger)
                pass
        except Exception as e:
            traceback.print_exc()
            logger.warning(f'receive invalid request. {e}')    

        return HttpResponse()