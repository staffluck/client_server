import socket
import argparse
import pickle
from time import sleep

IP = "localhost"
PORT = 5000


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]...",
    )
    parser.add_argument("-c", "--command",
                        help="Название задания(revert, shuffle, repeat)",
                        )
    parser.add_argument("-d", "--data",
                        help="Строка для задания",
                        )
    parser.add_argument("-ts", "--task-status",
                        help="ID задачи для получения статуса",
                        )
    parser.add_argument("-tr", "--task-response",
                        help="ID задачи для получения результата",
                        )
    parser.add_argument('-i', '--interactive',
                        help="Интерактивный режим(Пакетный)", action="store_true")
    parser.set_defaults(interactive=False)
    return parser


def send_request_get_response(connection: socket.socket, data: pickle.Pickler):
    connection.send(data)
    rd = connection.recv(1024)
    response = rd.decode()
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((IP, PORT))
    return response, connection


def main():
    parser = init_argparse()
    args = parser.parse_args()
    command = args.command
    data = args.data
    task_status_id = args.task_status
    task_response_id = args.task_response
    interactive = args.interactive

    if not all([command, data]) and not any([task_status_id, task_response_id]):
        print("Должны быть введены либо аргументы: --command и --data, либо --task-response или --task-status")
        return
    if all([task_status_id, task_response_id]):
        print("--task-response и --task-status выполняются отдельно")
        return

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((IP, PORT))

    if not interactive:
        if all([command, data]):
            request_data = pickle.dumps(["start", command, data])
        elif task_status_id:
            request_data = pickle.dumps(["status", task_status_id])
        elif task_response_id:
            request_data = pickle.dumps(["response", task_response_id])
        connection.send(request_data)
        rd = connection.recv(1024)
        print(rd.decode())
    else:
        start_request_data = pickle.dumps(["start", command, data])
        task_id, connection = send_request_get_response(connection, start_request_data)
        print(task_id)
        if task_id == "Не найдена команда под названием {}".format(command):
            return
        last_status = ""
        while True:
            status_request_data = pickle.dumps(["status", task_id])
            status, connection = send_request_get_response(connection, status_request_data)
            if last_status != status:
                last_status = status
                print(last_status)
                if last_status == "Завершено":
                    break
            sleep(2)
        response_request_data = pickle.dumps(["response", task_id])
        response, connection = send_request_get_response(connection, response_request_data)
        print(response)
    connection.close()


if __name__ == "__main__":
    main()
