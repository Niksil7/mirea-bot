class MarkupParser:
    def __init__(self, config):
        self.config = config

    async def get_buttons(self, language, buttons):
        return [i.split(';') for i in self.config[language][buttons].split('~')]

    async def get_text(self, language, text):
        return self.config[language][text].replace('\\n', '\n')