ALLOWED_HOSTS = [
    '*',
]
import os

WEBHOOK_SITE = os.getenv('WEBHOOK_SITE')

VIBER_BOT = {
    'ENABLE': False,
    "VIBER_AUTH_TOKEN": os.getenv('VIBER_AUTH_TOKEN', '<TOKEN_VIBER_BOT>'),
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX':'viber',  # (Optional[str]) # If this value is specified,
}

TELEGRAM_BOT = {
    'ENABLE': False,
    'MODE': 'WEBHOOK',
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': 'telegram',
    'TOKEN': os.getenv('TELEGRAM_TOKEN'),
    'PROXY': None
}

VK_BOT = {
    'ENABLE': True,
    'MODE': 'WEBHOOK',
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': 'vk',
    'CONFIRMATION_TOKEN': os.getenv('CONFIRMATION_TOKEN'),
    'API_TOKEN': os.getenv('API_TOKEN')
}

FACEBOOK_BOT = {
    'ENABLE': False,
    'MODE': 'WEBHOOK',
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': 'facebook',
    'ACCESS_TOKEN': '<FACEBOOK_ACCESS_TOKEN>',
    'VERIFY_TOKEN': '<FACEBOOK_VERIFY_TOKEN>'
}
