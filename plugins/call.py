from environment import Plugin
from utils import *


class Call(Plugin):
    name = 'Способ достучаться до человека'

    def check(self, event, vk):
        if is_message(event):
            message = get_lower_text(event)
            if len(message) > 1 and '/call' == message[0] and '@' in message[1]:
                for i in range(10):
                    send_message(event, vk, message[1])
                return True
        return False

