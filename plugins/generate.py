from environment import Plugin
import mc
from utils import *


class Generate(Plugin):
    name = 'Генератор заголовков панорамы'

    def __init__(self):
        sample = set()
        for line in open('headers.txt', 'r'):
            sample.add(line.split('\n')[0])
        self.generator = mc.StringGenerator(
            samples=list(sample)
        )

    def check(self, event, vk):
        if is_message(event) and get_lower_text(event) == '/generate':
            send_message(event, vk, self.generator.generate_string())
            return True
        return False
