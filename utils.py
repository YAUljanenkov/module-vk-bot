from vk_api.exceptions import VkApiError
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

def is_message(event):
    return event.type == VkBotEventType.MESSAGE_NEW


def get_lower_text(event):
    return event.object.get('text').lower()


def send_message(event, vk, text):
    vk.messages.send(peer_id=event.object['peer_id'], random_id=get_random_id(), message=text)
    return True


def kick_user(event, vk):
    vk.messages.removeChatUser(chat_id=event.object['peer_id'] - 2000000000,
                               member_id=event.object['reply_message']['from_id'])
    return event.object['reply_message']['from_id']


def get_commander(event):
    return event.object['from_id']


def get_conversation_members(event, vk):
    try:
        return vk.messages.getConversationMembers(peer_id=event.object['peer_id'])
    except VkApiError:
        return None


def get_replied_user(event):
    return event.object.get('reply_message', {}).get('from_id', None)
