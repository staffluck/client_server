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
                        help="ID задания",
                        )
    parser.add_argument("-d", "--data",
                        help="Строка для задания",
                        )
    parser.add_argument("-t", "--task",
                        help="ID задачи",
                        )
    # parser.add_argument('-i', '--interactive',
    #                     help="Интерактивный режим(Пакетный)")
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()
    command_id = args.command
    data = args.data
    task_id = args.task

    if not all([command_id, data]) and not task_id:
        print("Должны быть введены либо аргументы: --command и --data, либо --task")

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((IP, PORT))


    if all([command_id, data]):
        request_data = pickle.dumps([command_id, data])
    else:
        request_data = args.task.encode("utf-8")
    connection.send(request_data)
    rd = connection.recv(4096)
    try:
        print(pickle.loads(rd))
    except:
        print(rd.decode())
    connection.close()


if __name__ == "__main__":
    main()
