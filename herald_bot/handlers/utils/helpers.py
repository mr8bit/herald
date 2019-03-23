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

