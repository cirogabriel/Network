import sys
import socket
import threading

END = 'END'


def error(message):
    print(f'Error: {message}', file=sys.stderr)
    sys.exit(1)


def connect(host, port):
    print(f'Connecting to {host}:{port}')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print('Connected')

    username = input('Choose your username: ')
    s.sendall(username.encode())

    print(f'Type any message to send it, type {END} to finish')

    def receive_messages(sock):
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())

    threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

    while True:
        line = input()
        if line == END:
            break
        s.sendall(line.encode())

    print('Connection closed')
    s.close()


def main():
    if len(sys.argv) != 3:
        error(f'Usage: python {sys.argv[0]} host port')

    host = sys.argv[1]

    try:
        port = int(sys.argv[2])
    except ValueError:
        error(f'Invalid port {sys.argv[2]}')

    connect(host, port)


if __name__ == '__main__':
    main()
