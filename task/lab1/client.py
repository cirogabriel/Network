import socket
import threading
import sys

END = 'END'
BYTE = 1024


def error(message):
    print(f'Error: {message}', file=sys.stderr)
    sys.exit()


def receive_message(sock):
    while True:
        message = sock.recv(BYTE)
        if not message:
            break
        print(message.decode())


def connect(host, port):
    print(f'Conentando a {host}:{port}')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    print('[Conectado]')
    username = input('Ingresa nombre de usuario: ')
    client.sendall(username.encode())

    print(f'Escribe cualquier mensaje o {END} para terminar')

    threading.Thread(target=receive_message, args=(client, ), daemon=True).start()

    while True:
        message = input()
        if message == END:
            break
        client.sendall(message.encode())

    print('Conexion cerrada')

    socket.close()


def main():
    if len(sys.argv) != 3:
        print(f'Uso: python {sys.argv[0]} host port')

    host = sys.argv[1]

    try:
        port = sys.argv[2]
    except ValueError:
        error(f'puerto invalido {sys.argv[2]}')

    connect(host, port)


if __name__ == '__main__':
    main()
