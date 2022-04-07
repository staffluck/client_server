from abc import ABCMeta, abstractmethod
from uuid import uuid4
from time import sleep

registered_commands = {}

class ABCMeta_(ABCMeta):

    def __new__(cls, cls_name, bases, attrs):
        created_class = super().__new__(cls, cls_name, bases, attrs)
        if bases:  # Если это не BaseCommand
            registered_commands[attrs["name"]] = created_class
        return created_class


class BaseCommand(metaclass=ABCMeta_):

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process_data(self):
        pass


class RevertCommand(BaseCommand):
    name = "revert"
    simulated_delay = 2

    def process_data(self):
        return self.data[::-1]


class ShuffleCommand(BaseCommand):
    name = "shuffle"
    simulated_delay = 5

    def process_data(self):
        data = self.data
        shuffled_data = ""
        while data:
            pair = data[:2]
            shuffled_data += pair[::-1]
            data = data[2:]
        return shuffled_data


class RepeatCommand(BaseCommand):
    name = "repeat"
    simulated_delay = 7

    def process_data(self):
        result = ""
        for index, key in enumerate(self.data):
            result += (index + 1) * key
        return result


class CommandHandler:

    def __init__(self, data: str, command_name: str):
        self.data: str = data
        self.command_name: str = command_name
        self.status: str = "В очереди"
        self.response: str = None

        self.id: str = self.generate_unique_id()
        self.command: BaseCommand = self.get_command()(data)

    def process_data(self) -> None:
        self.status = "В искусственной задержке"
        self.simulate_delay()
        self.status = "Выполняется"
        data = self.command.process_data()
        self.status = "Завершено"
        self.response = data

    def encode(self, data) -> bytes:
        return data.encode("utf-8")

    def get_encoded_response(self) -> bytes:
        if self.response:
            return self.encode(self.response)
        else:
            return self.encode("Задача не выполнена! Её статус: {}".format(self.status))

    def get_encoded_status(self) -> bytes:
        return self.encode(self.status)

    def get_encoded_id(self) -> bytes:
        return self.encode(self.id)

    def generate_unique_id(self) -> str:
        return str(uuid4())

    def simulate_delay(self) -> None:
        sleep(self.command.simulated_delay)

    def get_command(self) -> BaseCommand:
        command = registered_commands.get(self.command_name)
        if command:
            return command
        raise Exception("Не найдена команда под названием {}".format(self.command_name))
