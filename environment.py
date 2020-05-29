from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
from private import VK_TOKEN, GROUP_ID, enable_logging
import os
import sys
from colored_logger import get_logger


class Bot:

    def __init__(self):
        vk_session = vk_api.VkApi(token=VK_TOKEN)
        self.vk = vk_session.get_api()
        self.longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
        self.plugins = []
        self.load_plugins()
        self.bot_logger = get_logger('Bot')

    def load_plugins(self):
        """This function initializes plugins."""
        ss = set(os.listdir('plugins'))
        sys.path.insert(0, 'plugins')

        for s in ss:
            if s != '__pycache__':
                __import__(os.path.splitext(s)[0], None, None, [''])
        for plugin in Plugin.__subclasses__():
            p = plugin()
            print('Added plugin', p)
            self.plugins.append(p)
            p.on_load()

    def loop(self):
        """Main process of the bot. """
        for event in self.longpoll.listen():
            print(event)
            for plugin in self.plugins:
                try:
                    if plugin.check(event, self.vk):
                        continue
                except Exception as e:
                    if enable_logging:
                        self.bot_logger.error(f'{plugin} crushed with error {e}')


class Plugin:
    name = ''

    def on_load(self):
        """
        Here you can do some preparatory work if __init()__ was not enough.

        :return: None.
        """
        pass

    def check(self, event, vk):
        """
        Do the main job here.

        :param event: Object that longpoll.listen() returns.
        :param vk: Object of the bot. It is adviced to use utils instead of the direct use.
        :return: True if Plugin did the job and False if not.
        """
        pass

    def __str__(self):
        return "<class 'Plugin' name '{0}'>".format(self.name)



