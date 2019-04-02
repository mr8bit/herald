ALLOWED_HOSTS = ['*', ]
import os

WEBHOOK_SITE = '<WEBHOOK_SITE_HERE>'

VIBER_BOT = {
    "VIBER_BOT_NAME": os.getenv('VIBER_BOT_NAME', '<NAME_BOT>'),
    "VIBER_AUTH_TOKEN": os.getenv('VIBER_AUTH_TOKEN', '<TOKEN_VIBER_BOT>'),
    "VIBER_AVATAR": os.getenv('VIBER_AVATAR', '<ULR_IMAGE_BOT>'),
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': '/viber',  # (Optional[str]) # If this value is specified,
}

DJANGO_TELEGRAMBOT = {
    'MODE': 'WEBHOOK',
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': '/bot',
    'BOTS': [
        {
            'TOKEN': '<TOKEN_TELEGRAM_BOT>',
        },
    ],
}

VK_BOT = {
    'MODE': 'WEBHOOK',
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': '/vk',
    'CONFIRMATION_TOKEN': '<VK_CONFIRMATION_TOKEN>',
    'API_TOKEN': '<VK_API_TOKEN>'
}

FACEBOOK_BOT = {
    'MODE': 'WEBHOOK',
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': '/facebook',
    'ACCESS_TOKEN': '<FACEBOOK_ACCESS_TOKEN>',
    'VERIFY_TOKEN': '<FACEBOOK_VERIFY_TOKEN>'
}
