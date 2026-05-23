from collections import deque
from difflib import SequenceMatcher


class MemoryManager:

    def __init__(self):
        self.short_memory = deque(maxlen=15)
        self.long_memory = {
            "nombre": None,
            "interacciones": []
        }
        self.state = None

    def store_short(self, text):
        self.short_memory.append(text)

        if "mi nombre es" in text.lower():
            self.long_memory["nombre"] = text.split()[-1].capitalize()

    def store_response(self, response):
        self.short_memory.append(response)
        self.long_memory["interacciones"].append(response)

    def retrieve_semantic(self, query):
        results = []

        for item in self.short_memory:
            score = SequenceMatcher(None, query, item).ratio()
            if score > 0.35:
                results.append(item)

        return "\n".join(results[-5:])

    def get_profile(self):
        return self.long_memory

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state