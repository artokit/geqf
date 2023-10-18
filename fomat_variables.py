VARIABLES = ['user_id']
CALLBACKS = {
    'check_reg': "Проверка регистрации на сайте."
}


def format_text(text: str, **kwargs) -> str:
    for var in VARIABLES:
        if '{' + var + '}' in text:
            text = text.replace('{' + var + '}', str(kwargs[var]))

    return text