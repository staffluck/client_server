import socket
import argparse
import pickle


IP = "localhost"
PORT = 5000


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]...",
    )
    parser.add_argument("-t", "--task",
                        help="ID задания",
                        required=True
                        )
    parser.add_argument("-d", "--data",
                        help="Строка для задания",
                        required=True
                        )
    # parser.add_argument('-i', '--interactive',
    #                     help="Интерактивный режим(Пакетный)")
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()
    task_id = args.task
    data = args.data

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((IP, PORT))

    request_data = pickle.dumps([task_id, data])

    connection.send(request_data)
    rd = connection.recv(4096)
    print(pickle.loads(rd))
    connection.close()


if __name__ == "__main__":
    main()
