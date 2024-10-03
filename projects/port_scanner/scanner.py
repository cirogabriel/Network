import socket
from concurrent.futures import ThreadPoolExecutor


def escanear_puerto_tcp(host, puerto):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            resultado = s.connect_ex((host, puerto))
            if resultado == 0:
                servicio = socket.getservbyport(
                    puerto, 'tcp') if puerto <= 1024 else 'Desconocido'
                return {"puerto": puerto, "estado": "abierto", "protocolo": "TCP", "servicio": servicio}
            else:
                return {"puerto": puerto, "estado": "cerrado", "protocolo": "TCP", "servicio": "Desconocido"}
    except Exception as e:
        print(f"Error al escanear el puerto TCP {puerto}: {e}")
        return {"puerto": puerto, "estado": "error", "protocolo": "TCP", "servicio": "Desconocido"}


def escanear_puerto_udp(host, puerto):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.9)
            s.sendto(b'', (host, puerto))

            try:
                _, _ = s.recvfrom(1024)
                servicio = socket.getservbyport(
                    puerto, 'udp') if puerto <= 1024 else 'Desconocido'
                return {"puerto": puerto, "estado": "abierto", "protocolo": "UDP", "servicio": servicio}
            except socket.timeout:
                return {"puerto": puerto, "estado": "abierto o filtrado", "protocolo": "UDP", "servicio": "Desconocido"}
            except socket.error:
                return {"puerto": puerto, "estado": "cerrado", "protocolo": "UDP", "servicio": "Desconocido"}
    except Exception as e:
        print(f"Error al escanear el puerto UDP {puerto}: {e}")
        return {"puerto": puerto, "estado": "error", "protocolo": "UDP", "servicio": "Desconocido"}


def escanear_puertos(host, puerto_inicio, puerto_fin, protocolo="TCP", hilos=500):
    puertos_abiertos = []

    with ThreadPoolExecutor(max_workers=hilos) as ejecutor:
        if protocolo == "TCP":
            tareas = [ejecutor.submit(escanear_puerto_tcp, host, puerto)
                      for puerto in range(puerto_inicio, puerto_fin + 1)]
        else:
            tareas = [ejecutor.submit(escanear_puerto_udp, host, puerto)
                      for puerto in range(puerto_inicio, puerto_fin + 1)]

        for tarea in tareas:
            resultado = tarea.result()
            if resultado and resultado['estado'] != "cerrado":
                puertos_abiertos.append(resultado)

    return puertos_abiertos
