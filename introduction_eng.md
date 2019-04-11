## Introduction

The template is based on the basic libraries for the messenger.
- python-telegram-bot
- viberbot
- vk-api
- https://github.com/qwe345asd/pymessenger

For facebook messenger, we have processed the old library.

This is a ready-made template that we can download and edit by replacing or adding to env tokens for our bot in different social networks.


The ways for knocking each messenger are specified in the `herald / local_settings.py` file. Each messenger has its own settings and its tokens. The token is required for bot authentication. WebHook
necessary to create a connection between the messenger server to receive messages.

> Webhook - event notification mechanism

Next comes the connection with the libraries in the `herald_bot / views.py` file, with the help of hendlers. After the request goes to processing in `herald_bot / handlers / * / request_handler.py`. In this file, an `instance` is created for
for further work.
 
 
Then a `StateMachine` is created, which processes the user’s state on different screens and remembers the last pressed button as an instance of the class.

`StateMachine` - works with the trigger, it unifies work with all messengers.


### Start

1. `git clone https://github.com/mr8bit/herald`
2. `cd herald`
2. `virtualenv venv --python=python3.6`
3. `pip install -r requirements.txt`
4. Replace tokens with your tokens
5. Run ngrok
6. Replace webhook with url received from ngrok
7. `python manage.py migrate`
8. `python manage.py runserver`