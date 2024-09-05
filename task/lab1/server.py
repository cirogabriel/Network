import socket
import threading
import sys

HOST = socket.gethostbyname(socket.gethostname())
BYTE = 1024
CODE = 'utf-8'
END = 'END'

connection = {}


def error(message):
    print(f'Error: {message}', file=sys.stderr)
    sys.exit(1)


def send_message(message, origin):
    for sock in connection.keys():
        if sock != origin:
            sock.sendall(message.encode())


def handle_client(sock, address):
    remote_socket = f'{address[0]}:{address[1]}'

    while True:
        try:
            message = sock.recv(BYTE).decode(CODE)
            if not message:
                break
            elif message not in connection:
                print(f'Username {message} establecida para la conexion {remote_socket}')
                connection[sock] = message
            elif message == END:
                connection.pop(sock, None)
                sock.close()
                break
            else:
                full_message = f'[{connection[sock]} -> {message}]'
                print(f'{remote_socket} -> {full_message}')
                send_message(full_message, sock)

        except socket.error as e:
            print(f'Conexion {remote_socket} -> {e}')
            break

    print(f'Conexion con {remote_socket} cerrada')
    sock.close()


def listen(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen()

    print(f'Escuchando en el puerto {port}')

    while True:
        client_socket, client_address = server.accept()
        remote_socket = f'{client_address[0]}:{client_address[1]}'
        print('Nueva conexion de ', remote_socket)
        client_socket.settimeout(60)
        client_socket.setblocking(True)

        cliente_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        cliente_thread.daemon = True
        cliente_thread.start()


def main():
    if len(sys.argv) != 2:
        error(f'Uso: python {sys.argv[0]} puerto')

    try:
        port = int(sys.argv[1])
    except ValueError:
        error(f'Puerto inválido: {sys.argv[1]}')

    listen(port)


if __name__ == '__main__':
    main()


