import socket
import sys
import threading

HOST = 'localhost'
END = 'END'

connection = {}


def error(message):
    print(f'Error: {message}', file=sys.stderr)
    sys.exit(1)


def send_message(message, origin):
    for sock in connection.keys():
        if sock != origin:
            sock.sendall(message.encode())


def listen(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen()

    print(f'Listening on port {port}')

    while True:
        client_socket, client_address = server.accept()
        remote_socket = f'{client_address[0]}:{client_address[1]}'
        print('New connection from', remote_socket)
        client_socket.settimeout(60)
        client_socket.setblocking(True)

        def handle_client(socket, address):
            remote_socket = f'{address[0]}:{address[1]}'
            while True:
                try:
                    message = socket.recv(1024).decode('utf-8')
                    if not message:
                        break

                    if socket not in connection:
                        print(
                            f'Username {message} set for connection {remote_socket}')
                        connection[socket] = message
                    elif message == END:
                        connection.pop(socket, None)
                        socket.close()
                        break
                    else:
                        full_message = f'[{connection[socket]}]: {message}'
                        print(f'{remote_socket} -> {full_message}')
                        send_message(full_message, socket)
                except socket.error as e:
                    print(f'Connection {remote_socket} -> {e}')
                    break

            print(f'Connection with {remote_socket} closed')
            socket.close()

        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.daemon = True
        client_thread.start()


def main():
    if len(sys.argv) != 2:
        error(f'Usage: python {sys.argv[0]} port')

    try:
        port = int(sys.argv[1])
    except ValueError:
        error(f'Invalid port {sys.argv[1]}')

    listen(port)


if __name__ == '__main__':
    main()
