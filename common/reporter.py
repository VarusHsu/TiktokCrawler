import time


class Reporter:
    container: dict
    time_container: dict

    def __init__(self):
        self.container = {}
        self.time_container = {}

    def init_counter(self, name: str):
        self.container[name] = 0

    def self_increase(self, name: str):
        self.container[name] += 1

    def get_counter(self, name: str) -> int:
        return self.container[name]

    def set_counter(self, name: str, value: int):
        self.container[name] = value

    def set_timer(self, name: str = ""):
        self.time_container[name] = int(time.time() * 1000)

    def get_during(self, name: str = "") -> int:
        return int(time.time() * 1000) - self.time_container[name]
