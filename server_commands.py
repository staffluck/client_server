from abc import ABCMeta, abstractmethod
from uuid import uuid4
from time import sleep


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


class RepeatCommand(BaseCommand):
    simulated_delay = 7

    def process_data(self):
        result = ""
        for index, key in enumerate(self.data):
            result += (index + 1) * key
        return result


class CommandHandler:

    def __init__(self, data: str, command_id: int):
        self.data: str = data
        self.command_id: int = command_id
        self.status: str = "В очереди"
        self.response: str = None

        self.id: str = self.generate_unique_id()
        self.command: BaseCommand = self.get_command()(data)

    def process_data(self):
        self.status = "В искусственной задержке"
        print("HELLO")
        self.simulate_delay()
        print("HELLO")
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

    def generate_unique_id(self) -> uuid4:
        return str(uuid4())

    def simulate_delay(self):
        sleep(self.command.simulated_delay)

    def get_command(self) -> BaseCommand:
        if self.command_id == 1:
            return RevertCommand
        elif self.command_id == 2:
            return ShuffleCommand
        elif self.command_id == 3:
            return RepeatCommand
        raise Exception("Неизвестная команда")
