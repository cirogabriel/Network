from socket import *

idServidor = 'localhost'
puertoServidor = 12000

socketCliente = socket(AF_INET, SOCK_DGRAM)

mensaje = input('Entrar una sentencia en minúsculas: ')

socketCliente.sendto(mensaje.encode(), (idServidor, puertoServidor))

mensajeModificado, direccionServidor = socketCliente.recvfrom(2048)

print('Socket del servidor = ', direccionServidor)
print(mensajeModificado.decode())

socketCliente.close()
