import socket
import argparse
import pickle


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
    parser.add_argument
    # parser.add_argument('-i', '--interactive',
    #                     help="Интерактивный режим(Пакетный)")
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()
    command = args.command
    data = args.data
    task_status_id = args.task_status
    task_response_id = args.task_response

    if not all([command, data]) and not any([task_status_id, task_response_id]):
        print("Должны быть введены либо аргументы: --command и --data, либо --task")
        return
    if all([task_status_id, task_response_id]):
        print("--task-response и --task-status выполняются отдельно")
        return

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((IP, PORT))

    if all([command, data]):
        request_data = pickle.dumps(["start", command, data])
    elif task_status_id:
        request_data = pickle.dumps(["status", task_status_id])
    elif task_response_id:
        request_data = pickle.dumps(["response", task_response_id])
    connection.send(request_data)
    rd = connection.recv(4096)
    print(rd.decode())

    connection.close()


if __name__ == "__main__":
    main()
