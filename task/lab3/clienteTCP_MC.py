from socket import *

idServidor = 'localhost'
puertoServidor = 12000

socketCliente = socket(AF_INET, SOCK_STREAM)
socketCliente.connect((idServidor, puertoServidor))

print(f'[CLIENTE] Conectado al servidor {idServidor}:{puertoServidor} desde {socketCliente.getsockname()}')

mensaje = input('Entrar un mensaje en minúsculas: ')

while mensaje != "":
    socketCliente.send(mensaje.encode())
    print(f'[CLIENTE] Mensaje enviado: {mensaje}')

    mensajeModificado = socketCliente.recv(1024)
    print(f'[CLIENTE] Respuesta del servidor: {mensajeModificado.decode()}')

    mensaje = input('Entrar un mensaje en minusculas: ')

socketCliente.close()
print(f'[CLIENTE] Conexion cerrada con el servidor {idServidor}:{puertoServidor}')
