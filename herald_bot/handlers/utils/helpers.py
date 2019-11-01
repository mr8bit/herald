import logging
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
logger = logging.getLogger(__name__)

def make_keyboard(buttons):
    button_main_property = {
        "ActionType": "reply",
        "TextVAlign": "middle",
        "TextHAlign": "center",
        "TextOpacity": 60,
        "TextSize": "regular",
        "BgColor" : "#9A999B"
    }

    keyboard = {
        "Type" : "keyboard",
        "Buttons": [
            {
                "ActionBody": button_text,
                "Text": button_text,
                **button_main_property
            } for button_text in buttons
        ]
    }

    return keyboard

def divide_chunks(l, n=1):
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
  

def make_keyboard_vk(buttons):
    if len(buttons) > 40:
        logger.error("Error on create keyboard: Too many butons")
        return ''
    
    keyboard = VkKeyboard(one_time=True)
    lines = list(divide_chunks(buttons))

    for line in lines[:-1]:
        for b in line:
             keyboard.add_button(b)
        keyboard.add_line() 

    for b in lines[-1]:
             keyboard.add_button(b)
    
    return keyboard.get_keyboard()