from django.conf import settings
from django.urls import path

from . import views

webhook_base = settings.TELEGRAM_BOT.get('WEBHOOK_PREFIX', '/')

if webhook_base.startswith("/"):
    webhook_base = webhook_base[1:]
if not webhook_base.endswith("/"):
    webhook_base += "/"

urlpatterns = [
    path('{}/'.format(settings.VIBER_BOT.get("WEBHOOK_PREFIX")), views.viber_bot, name='webhook_viber'),

    path('{}<str:bot_token>/'.format(webhook_base), views.webhook, name='webhook_telegram'),

    path('{0}'.format(settings.VK_BOT.get("WEBHOOK_PREFIX")), views.vk_bot, name='webhook_vk'),

    path('{0}'.format(settings.FACEBOOK_BOT.get("WEBHOOK_PREFIX")), views.facebook_bot, name='webhook_facebook'),
]

