import json
import logging
import sys

import telegram
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram.error import (TelegramError)

from herald_bot.apps import DjangoTelegramBot
from herald_bot.handlers.viber.request_handler import ViberRequestHandler

from herald_bot.handlers.vk.request_handler import VKRequestHandler
from herald_bot.handlers.facebook.request_handler import FacebookRequestHandler

logger = logging.getLogger(__name__)
import json

@csrf_exempt
def viber_bot(request):
    """
        Урл для работы вайбера
    :param request:
    :return:
    """
    if request.method == 'POST':
        viber_request_handler = ViberRequestHandler.create_instance()
        response = viber_request_handler.parse(request)
    return HttpResponse()
import json
import datetime
@csrf_exempt
def vk_bot(request):
    """
        Урл для работы vk
    :param request:
    :return:
    """

    if request.method == 'POST':
        vk_request_handler = VKRequestHandler.create_instance()
        response = vk_request_handler.parse(request)
        return response
    return HttpResponse('Ok')

@csrf_exempt
def facebook_bot(request):
    """
        Урл для работы facebook
    :param request:
    :return:
    """
    facebook_request_handler = FacebookRequestHandler.create_instance()
    response = facebook_request_handler.parse(request)
    return response

@csrf_exempt
def webhook(request, bot_token):
    """
        Вебхук для телеграмма
    :param request:
    :param bot_token:
    :return:
    """
    bot = DjangoTelegramBot.getBot(bot_id=bot_token, safe=False)
    if bot is None:
        logger.warning('Request for not found token : {}'.format(bot_token))
        return JsonResponse({})

    try:
        data = json.loads(request.body.decode("utf-8"))

    except:
        logger.warning('Telegram bot <{}> receive invalid request : {}'.format(bot.username, repr(request)))
        return JsonResponse({})

    dispatcher = DjangoTelegramBot.getDispatcher(bot_token, safe=False)
    if dispatcher is None:
        logger.error('Dispatcher for bot <{}> not found : {}'.format(bot.username, bot_token))
        return JsonResponse({})

    try:
        update = telegram.Update.de_json(data, bot)
        dispatcher.process_update(update)
        logger.debug('Bot <{}> : Processed update {}'.format(bot.username, update))
    # Dispatch any errors
    except TelegramError as te:
        logger.warning("Bot <{}> : Error was raised while processing Update.".format(bot.username))
        dispatcher.dispatchError(update, te)

    # All other errors should not stop the thread, just print them
    except:
        logger.error("Bot <{}> : An uncaught error was raised while processing an update\n{}".format(bot.username,
                                                                                                     sys.exc_info()[0]))

    finally:
        return JsonResponse({})
