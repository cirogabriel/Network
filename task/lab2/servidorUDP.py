from socket import *

puertoServidor = 12000
socketServidor = socket(AF_INET, SOCK_DGRAM)
socketServidor.bind(('', puertoServidor))

print('El servidor está listo para recibir')

while True:
    mensaje, direccionCliente = socketServidor.recvfrom(2048)
    mensajeModificado = mensaje.decode().upper()
    socketServidor.sendto(mensajeModificado.encode(), direccionCliente)

