import socket
import threading


class HiloCliente(threading.Thread):
    def __init__(self, ip, puerto, socketCnx):
        threading.Thread.__init__(self)
        self.ip = ip
        self.puerto = puerto
        self.socketCnx = socketCnx
        print(f'[SERVIDOR] Nueva conexion desde {self.ip}:{self.puerto}')

    def run(self):
        while True:
            mensaje = self.socketCnx.recv(1024).decode()
            if not mensaje:
                break
            print(f'[SERVIDOR] Hilo: {threading.current_thread().name}, Mensaje recibido: {mensaje}')
            mensajeCapitalizado = mensaje.upper()
            self.socketCnx.send(mensajeCapitalizado.encode())
            print(f'[SERVIDOR] Mensaje enviado a {self.ip}:{self.puerto}')

        self.socketCnx.close()
        print(f'[SERVIDOR] Conexion cerrada con {self.ip}:{self.puerto}')
