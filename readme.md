## Herald - one for all
Herald - one bot, many messengers

Choose language: [:us:](readme.md) [:ru:](readme_rus.md)

 

The project is under development and is not a stable version.

Currently the project only supports:
- <img src="https://www.securitylab.ru/upload/iblock/65d/65d8b265716611fc4358aeb0a2b3e56e.png" width="25"> Viber 
- <img src="https://lh3.googleusercontent.com/u1DT1-_6FLTqldVf9fplZoMQ2leaP-Szgej3AuGXOjmUbaTbWWu8OxURE3QtmEgxam20R7yr3Q=w128-h128-e365" width="25"> Telegram 
- <img src="http://primrep.ru/wp-content/uploads/2017/02/VK.jpg" width="25"> Vk
- <img src="https://infoinspired.com/wp-content/uploads/2014/02/facebook-friends.png" width="25"> Facebook

In the plans: 

- <img src="https://cdn6.aptoide.com/imgs/4/6/1/461638042f6303c2860627f842116ccd_icon.png?w=256" width="25"> WhatsApp

How to use?

The first step is to configure the project in the file `herald/local_settings.py` must be set 
`WEBHOOK_SITE` - This is a regular encrypted URL `https` (for the first run and development can use [ngrok](https://ngrok.com/))
```python
WEBHOOK_SITE = '<WEBHOOK_SITE_HERE>' 
```
##### Viber setup
Set Viber tokens and other variables
 
```python
VIBER_BOT = {
    "VIBER_BOT_NAME": os.getenv('VIBER_BOT_NAME', '<NAME_BOT_HERE>'),
    "VIBER_AUTH_TOKEN": os.getenv('VIBER_AUTH_TOKEN', '<TOKEN_VIBER_BOT_HERE>'),
    "VIBER_AVATAR": os.getenv('VIBER_AVATAR', '<ULR_IMAGE_BOT_HERE>'),
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': '/viber',  # (Optional[str]) # If this value is specified,
}
```
##### Telegram settings

To set up a Telegram bot, just set a token and all 

```python
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
```

##### Facebook settings

Setting up a Facebook bot is a hassle.

Facebook support based on this library:
https://github.com/qwe345asd/pymessenger

```
pip install git+https://github.com/qwe345asd/pymessenger
```

```python
FACEBOOK_BOT = {
    'MODE': 'WEBHOOK',
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': '/facebook',
    'ACCESS_TOKEN': '<FACEBOOK_ACCESS_TOKEN>',
    'VERIFY_TOKEN': '<FACEBOOK_VERIFY_TOKEN>'
}

```

##### About code

User login is in the file `herald_bot/states/main.py` in class `BootStrapState`.

```python
class BootStrapState(State):
    def on_enter(self, trigger):
        """It works when a user enters a new state / screen / class"""
        pass
        
    def on_trigger(self, trigger):
        """Handles keystrokes / text sent"""
        trigger.send_message("Hi, this is a Herald, I'm alone and everywhere")
        return BootStrapState() # Transition to another state / screen / class
        
    def on_exit(self, trigger):
        """It works when the user enters the new state / screen / class"""
        pass
```

How to send messages? And what is in the triger?

```python
trigger.text # Text from user 
trigger.messenger # the messenger from which the message came 0 - Telegram 1 - Viber 
trigger.user_id # id user/chat, chat_id in Telegram, user_id in Viber 
trigger.state # user state, class instance  
trigger.get_user() # Returns a user from bd Django model
trigger.create_user() # Create user
trigger.send_photo(image_path) # Send photos image_path - photo path
trigger.send_message(message) # Posting a message message - Message text
trigger.send_keyboard(message, buttons) # Send a message with the keyboard message - Message text buttons - text array
```

Based on libraries:
- [django-telegrambot](https://github.com/JungDev/django-telegrambot)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [viber-bot-python](https://github.com/Viber/viber-bot-python)
- [vk_api](https://github.com/python273/vk_api)

