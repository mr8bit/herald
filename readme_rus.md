## Herald - один за всех
Herald - один бот для всех мессенджеров

Выберите язык:  [:us:](readme.md) [:ru:](readme_rus.md)

Проект находится на стадии развития и не является стабильной версией

В данный момент проект поддерживает только:
- <img src="https://www.securitylab.ru/upload/iblock/65d/65d8b265716611fc4358aeb0a2b3e56e.png" width="25"> Viber 
- <img src="https://lh3.googleusercontent.com/u1DT1-_6FLTqldVf9fplZoMQ2leaP-Szgej3AuGXOjmUbaTbWWu8OxURE3QtmEgxam20R7yr3Q=w128-h128-e365" width="25"> Telegram 

В планах: 
- <img src="http://primrep.ru/wp-content/uploads/2017/02/VK.jpg" width="25"> Vk
- <img src="https://infoinspired.com/wp-content/uploads/2014/02/facebook-friends.png" width="25"> Facebook
- <img src="https://cdn6.aptoide.com/imgs/4/6/1/461638042f6303c2860627f842116ccd_icon.png?w=256" width="25"> WhatsApp


Как пользоваться?


Первым шагом надо настроить проект, в файле `herald/local_settings.py` необходимо задать 
`WEBHOOK_SITE` - это обычный URL с шифрованием `https` (для первого запуска и разработки можете использовать [ngrok](https://ngrok.com/))
```python
WEBHOOK_SITE = '<WEBHOOK_SITE_HERE>' 
```
##### Настрока Viber
Задать токены для Viber и остальные переменные
 
```python
VIBER_BOT = {
    "VIBER_BOT_NAME": os.getenv('VIBER_BOT_NAME', '<NAME_BOT_HERE>'),
    "VIBER_AUTH_TOKEN": os.getenv('VIBER_AUTH_TOKEN', '<TOKEN_VIBER_BOT_HERE>'),
    "VIBER_AVATAR": os.getenv('VIBER_AVATAR', '<ULR_IMAGE_BOT_HERE>'),
    'WEBHOOK_SITE': WEBHOOK_SITE,
    'WEBHOOK_PREFIX': '/viber',  # (Optional[str]) # If this value is specified,
}
```
##### Настрока Telegram

Для настройки Telegram бота достаточно задать токен и все 

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

##### Разбор кода

Вход пользователя осуществляется в файле `herald_bot/states/main.py` в классе `BootStrapState`.
```python
class BootStrapState(State):
    def on_enter(self, trigger):
        """Срабатывает при входе пользователя в новое состояние/экран/класс"""
        pass
        
    def on_trigger(self, trigger):
        """Обрабатывает нажатия кнопок"""
        trigger.send_message("Привет, это Herald, я один и я везде")
        return BootStrapState() # Переход в другое состояние/экран/класс
        
    def on_exit(self, trigger):
        """Срабатывает при выходе пользователя в новое состояние/экран/класс"""
        pass
```

Как отправлять сообщения? И что находиться в тригере?

```python
trigger.text # Текст от пользователя 
trigger.messenger # месенджер от которого пришло сообщение 0 - Telegram 1 - Viber 
trigger.user_id # id пользователя/чата chat_id в Телеграм user_id в Viber 
trigger.state # состояние пользователя, экземпляр класса  
trigger.get_user() # Возвращяет пользователя из bd Django model
trigger.create_user() # Создание пользователя
trigger.send_photo(image_path) # Отправка фотографии image_path - путь к фотографии
trigger.send_message(message) # Отправка сообщения message - текст сообщения
trigger.send_keyboard(message, buttons) # Отправка сообщения c клавиатурой message - текст сообщения buttons - массив кнопок
```


Основаны на библиотеках:
- [django-telegrambot](https://github.com/JungDev/django-telegrambot)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [viber-bot-python](https://github.com/Viber/viber-bot-python)
