from environment import Plugin
from utils import *
import vk_api
from colored_logger import get_logger
from private import enable_logging


class Kick(Plugin):
    name = 'Исключение пользователя'

    def __init__(self):
        self.logger = get_logger('Kick Plugin')

    def check(self, event, vk):
        if is_message(event) and get_lower_text(event) == '/kick':
            try:
                members = get_conversation_members(event, vk)
                if not members:
                    send_message(event, vk, f"Мне нужны права администратора, чтобы исключать других пользователей.")
                    return True

                user = get_replied_user(event)
                if not user:
                    send_message(event, vk, f"Эта команда должна быть ответом на другое сообщение.")
                    return True

                commander = get_commander(event)
                commander_data = list(filter(lambda x: x['member_id'] == commander, members['items']))
                if commander_data and not commander_data[0].get('is_admin', False):
                    send_message(event, vk, f"Эту команду могут использовать только администраторы.")
                    return True

                target_data = list(filter(lambda x: x['member_id'] == user, members['items']))
                if target_data and target_data[0].get('is_admin', False):
                    send_message(event, vk, f"Нельзя исключать администраторов.")
                    return True

                kick_user(event, vk)
                send_message(event, vk, f"[id{user}|Пользователь] был исключён.")
            except vk_api.exceptions.ApiError as e:
                if enable_logging:
                    self.logger.error(f'vk_api error {e}')
                send_message(event, vk, f"Хмм, что-то пошло не так.")
            return True
        return False
