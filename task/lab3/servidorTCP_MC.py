import socket
import hiloClienteTCP

idServidor = ''
puertoServidor = 12000

socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socketServidor.bind((idServidor, puertoServidor))
socketServidor.listen(1)

print('El servidor esta listo para escuchar')

while True:
    (socketConexion, (ipCliente, puertoCliente)) = socketServidor.accept()
    print(f'[SERVIDOR] Conexion establecida con {ipCliente}:{puertoCliente}')
    hilo = hiloClienteTCP.HiloCliente(ipCliente, puertoCliente, socketConexion)
    hilo.start()

socketServidor.close()
