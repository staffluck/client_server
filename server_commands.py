from abc import ABCMeta, abstractmethod
from uuid import uuid4

class BaseCommand(metaclass=ABCMeta):

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process_data(self):
        pass


class RevertCommand(BaseCommand):
    simulated_delay = 2

    def process_data(self):
        return self.data[::-1]


class ShuffleCommand(BaseCommand):
    simulated_delay = 5

    def process_data(self):
        data = self.data
        shuffled_data = ""
        while data:
            pair = data[:2]
            shuffled_data += pair[::-1]
            data = data[2:]
        return shuffled_data


class CommandHandler:

    def __init__(self, data: str, command_id: int):
        self.data: str = data
        self.command_id: int = command_id
        self.status: str = "Выполняется"
        self.response: str = None

        self.id: str = self.generate_unique_id()
        self.command: BaseCommand = self.get_command()(data)

    def encode(self, data) -> bytes:
        return data.encode("utf-8")

    def get_encoded_response(self) -> bytes:
        return self.encode(self.response)

    def get_encoded_status(self) -> bytes:
        return self.encode(self.status)

    def get_encoded_id(self) -> bytes:
        return self.encode(self.id)

    def generate_unique_id(self) -> uuid4:
        return str(uuid4())

    def get_command(self) -> BaseCommand:
        if self.command_id == 1:
            return RevertCommand
        elif self.command_id == 2:
            return ShuffleCommand
        elif self.command_id == 3:
            return ShuffleCommand
        raise Exception("Неизвестная команда")
